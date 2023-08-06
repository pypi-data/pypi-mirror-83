from typing import Callable

import structlog

from diffusion.components import Component
from diffusion import datatypes as dt
from diffusion.internal.services.topics import (
    FallbackStreamHandlerKey,
    TOPICS_DATA_KEY,
    Topic,
    ValueStreamHandlerKey,
)
from .selectors import get_selector

LOG = structlog.get_logger()


class Topics(Component):
    """ Topics component. """

    @property
    def topics(self) -> dict:
        """ Internal storage for registered topics. """
        return self.session.data[TOPICS_DATA_KEY]

    def add_value_stream(
        self,
        topic_selector: str,
        topic_type: dt.DataTypeArgument,
        update: Callable,
        **kwargs: Callable,
    ) -> None:
        """ Registers a value stream handler for a topic selector and type.

            A value stream is a series of events associated with a registered topic. This
            method makes it possible to register callbacks for each of those events.

            Args:
                topic_selector: The handler will react to the updates to all topics matching
                                this selector.
                topic_type: The data type of the topic being streamed.
                update: The callback to be executed on the value update event.
                **kwargs: The callbacks to be executed on other value stream events.
                          The following events are currently supported:
                            * subscribe
                            * unsubscribe
                            * error
                            * close
        """
        topic_type = dt.get(topic_type)
        kwargs["update"] = update
        self.session.handlers.update(
            {
                ValueStreamHandlerKey(
                    event=event.lower(), selector=get_selector(topic_selector), type=topic_type
                ): callback
                for event, callback in kwargs.items()
            }
        )

    def add_fallback_stream(
        self, topic_type: dt.DataTypeArgument, update: Callable, **kwargs: Callable,
    ) -> None:
        """ Registers a fallback stream handler for a topic type.

            A value stream is a series of events associated with a registered topic. This
            method makes it possible to register callbacks for each of those events.

            Args:
                topic_type: The data type of the topic being streamed.
                update: The callback to be executed on the value update event.
                **kwargs: The callbacks to be executed on other value stream events.
                          The following events are currently supported:
                            * subscribe
                            * unsubscribe
                            * error
                            * close
        """
        topic_type = dt.get(topic_type)
        kwargs["update"] = update
        self.session.handlers.update(
            {
                FallbackStreamHandlerKey(event=event.lower(), type=topic_type): callback
                for event, callback in kwargs.items()
            }
        )

    async def subscribe(self, topic_selector: str):
        """ Register the session to receive updates for the given topic.

            Args:
                topic_selector: The selector for topics to subscribe to.
        """
        service = self.services.SUBSCRIBE
        service.request.set(topic_selector)
        response = await self.session.send_request(service)
        return response

    async def unsubscribe(self, topic_selector: str):
        """ Unregister the session to stop receiving updates for the given topic.

            Args:
                topic_selector: The selector for topics to unsubscribe from.
        """
        service = self.services.UNSUBSCRIBE
        service.request.set(topic_selector)
        response = await self.session.send_request(service)
        return response
