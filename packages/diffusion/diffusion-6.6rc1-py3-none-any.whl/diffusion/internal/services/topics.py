""" Topic services module. """
from __future__ import annotations

import asyncio
import io
from collections import defaultdict, namedtuple
from enum import IntEnum
from typing import Callable, cast, Iterator, MutableMapping, Optional, Set, TYPE_CHECKING, Union

import attr
import cbor2 as cbor
import structlog

from diffusion import datatypes as dt
from diffusion.internal.serialisers import get_serialiser
from diffusion.internal.utils import coroutine
from .abstract import InboundService, OutboundService

if TYPE_CHECKING:  # pragma: no cover
    from diffusion.internal.session import InternalSession, HandlersMapping

LOG = structlog.get_logger()

TOPICS_DATA_KEY = "topics"


class ValueStreamHandlerKey(namedtuple("ValueStreamHandlerKey", "event selector type")):
    """ The compound key for value stream handlers in handlers registry.

        Args:
            event: The string specifying topic event, like `update` or `subscribe`.
            selector: The Selector instance with the registered selector.
            type: The topic type being registered.
     """

    __slots__ = ()


class FallbackStreamHandlerKey(namedtuple("FallbackStreamHandlerKey", "event type")):
    """ The compound key for fallback stream handlers in handlers registry.

        Args:
            event: The string specifying topic event, like `update` or `subscribe`.
            type: The topic type being registered.
     """

    __slots__ = ()


@attr.s(on_setattr=attr.setters.frozen, slots=True, auto_attribs=True)
class Topic:
    """ A Diffusion topic.

        Args:
            id: Internal ID of the topic on this session.
            path: The topic path.
            type: Type of the topic.
            properties: A mapping of topic properties.
            binary_value: The current value of the property. `None` by default.
            streams: A mapping of streams available for various events.
    """

    CBOR_NULL_VALUE = b"\xf6"

    id: int
    path: str
    type: dt.DataType = attr.ib(converter=dt.get)
    properties: MutableMapping = attr.ib(converter=dict, default={})
    binary_value: Optional[bytes] = attr.ib(on_setattr=attr.setters.NO_OP, default=None)
    streams: MutableMapping[str, Set[Callable]] = attr.ib(
        on_setattr=attr.setters.NO_OP, default=attr.Factory(lambda: defaultdict(set))
    )

    @property
    def value(self):
        """ Returns the current value for the topic. """
        if self.binary_value is None:
            return None
        return self.type.from_bytes(self.binary_value).value

    def update_streams(self, handlers: HandlersMapping) -> None:
        """ Updates the collection of registered stream handlers for the topic.

            First it tries to locate any registered handlers with selectors that
            match the topic's path and type. If none are available, it selects
            the fallback stream handlers which match the topic's type.

            Args:
                handlers: The `Session.handlers` mapping containing all the registered handlers.
        """
        for key, handler in handlers.items():
            if (
                isinstance(key, ValueStreamHandlerKey)
                and key.type is self.type
                and key.selector.match(self.path)
            ):
                self.streams[key.event].add(coroutine(handler))
        if not any(map(len, self.streams.items())):
            # include fallback streams
            for key, handler in handlers.items():
                if isinstance(key, FallbackStreamHandlerKey) and key.type is self.type:
                    self.streams[key.event].add(coroutine(handler))

    async def handle(self, event: str, **kwargs) -> None:
        """ Runs registered stream handlers for the topic and event.

            Args:
                event: Textual identifier for the event: `update`, `subscribe` etc.
                kwargs: Various parameters. The topic's path and current value are
                        injected at runtime.
        """
        handlers = self.streams[event]
        if handlers:
            kwargs.update({"topic_path": self.path, "topic_value": self.value})
            await asyncio.wait([handler(**kwargs) for handler in handlers])
        else:
            LOG.debug("No handlers registered for topic/event.", topic=self, stream_event=event)

    def update(self, value: bytes, is_delta=False) -> None:
        """ Updates the binary value of the topic.

            Args:
                value: The new binary value to apply.
                is_delta: If `True`, the new binary value is a binary delta to be
                       applied to the current value. If `False`, the current value
                       is replaced by the new value.
        """
        LOG.debug("Applying binary value.", value=value, is_delta=is_delta)
        if is_delta:
            value = self.apply_delta(cast(bytes, self.binary_value), value)
        self.binary_value = value

    @classmethod
    def apply_delta(cls, original: bytes, delta: bytes) -> bytes:
        """ Applies a binary delta value to an original binary value.

            Args:
                original: The original binary value.
                delta: The binary delta value to apply. If this value is the CBOR
                       null value, the original value is left unchanged.
        """
        if delta == cls.CBOR_NULL_VALUE:
            return original
        new_value = b"".join(
            chunk if isinstance(chunk, bytes) else original[chunk]
            for chunk in cls.parse_delta(delta)
        )
        LOG.debug("Applying binary delta.", original=original, delta=delta, new=new_value)
        return new_value

    @classmethod
    def parse_delta(cls, delta: bytes) -> Iterator[Union[bytes, slice]]:
        """ Parses a binary delta value, yielding insert and match values.

            The yielded values are either bytes to apply, or slices to be
            extracted from the original value.

            Args:
                delta: The binary delta to parse.
        """
        LOG.debug("Parsing binary delta.", delta=delta)
        length = len(delta)
        offset = 0
        match = None
        while offset < length:
            chunk = cbor.loads(delta[offset:])
            if isinstance(chunk, bytes):
                yield chunk
            elif match is None:
                match = chunk
            else:
                yield slice(match, match + chunk)
                match = None
            offset += len(cbor.dumps(chunk))


class Subscribe(OutboundService):
    """ Subscribe service. """

    service_id = 3
    name = "SUBSCRIBE"
    request_serialiser = get_serialiser("string")
    response_serialiser = get_serialiser("void")


class Unsubscribe(OutboundService):
    """ Unsubscribe service. """

    service_id = 4
    name = "UNSUBSCRIBE"
    request_serialiser = get_serialiser("string")
    response_serialiser = get_serialiser("void")


class NotifySubscription(InboundService):
    """ Topic subscription notification using TopicSpecification. """

    service_id = 87
    name = "NOTIFY_SUBSCRIPTION"
    request_serialiser = get_serialiser("protocol14-topic-specification-info")
    response_serialiser = get_serialiser()
    event = "subscribe"

    async def consume(self, stream: io.BytesIO, session: InternalSession) -> None:
        """ Receive the request from the server. """
        await super().consume(stream, session)
        topics = session.data[TOPICS_DATA_KEY]
        topic_id = self.request["topic-id"]
        if topic_id in topics:
            topic = topics[topic_id]
            log_message = "Resubscribed to topic."
        else:
            topic = Topic(*self.request.values())
            topics[topic_id] = topic
            log_message = "Subscribed to topic."
        topic.update_streams(session.handlers)
        LOG.debug(log_message, topic=topic)
        await topic.handle(self.event)


class NotifyUnsubscription(InboundService):
    """ Topic unsubscription notification. """

    service_id = 42
    name = "NOTIFY_UNSUBSCRIPTION"
    request_serialiser = get_serialiser("protocol14-unsubscription-notification")
    response_serialiser = get_serialiser()
    event = "unsubscribe"

    async def consume(self, stream: io.BytesIO, session: InternalSession) -> None:
        """ Receive the request from the server. """
        await super().consume(stream, session)
        topics = session.data[TOPICS_DATA_KEY]
        topic_id = self.request["topic-id"]
        reason = UnsubscribeReason(self.request[1])
        if topic_id in topics:
            topic = topics[topic_id]
            LOG.debug("Unsubscribed from topic.", topic=topic, reason=reason)
            await topic.handle(self.event, reason=reason)
        else:
            LOG.warning("Unknown topic.", topic_id=topic_id)


class UnsubscribeReason(IntEnum):
    """ Unsubscribe reason ID values. """

    REQUESTED = 0
    CONTROL = 1
    REMOVAL = 2
    AUTHORIZATION = 3
    UNKNOWN_UNSUBSCRIBE_REASON = 4
    BACK_PRESSURE = 5

    def __str__(self):
        return self.name
