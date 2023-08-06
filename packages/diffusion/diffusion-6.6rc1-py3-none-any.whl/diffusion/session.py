""" Public session for end users.

    @author: Push Technology Limited
"""
from __future__ import annotations

import sys
from typing import Callable, cast, Dict, Hashable, Optional

import structlog

from diffusion.internal.exceptions import DiffusionError
from diffusion.internal.session import Connection, Credentials, InternalSession

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

ANONYMOUS_PRINCIPAL = ""


class Session:
    """ A client session connected to a Diffusion server or a cluster of servers.

        Args:
            url: WebSockets URL of the Diffusion server to connect to.
            principal: The name of the security principal associated with the session.
            credentials: Security information required to authenticate the connection.

        The recommended method is to instantiate this class as an async context manager.
        Here is a minimal example:

            async with diffusion.Session("ws://diffusion.server:8080") as session:
                # do some work with the session

        The context manager will make sure that the connection is properly closed at
        the end of the program. Alternatively, it is possible to open the connection
        explicitly, which can be useful if the session needs to be passed around, in
        this case the connection needs to be explicitly closed as well:

            session = diffusion.Session("ws://diffusion.server:8080")
            await session.connect()
            # do some work with the session
            await session.close()
    """

    def __init__(
        self,
        url: str,
        principal: str = ANONYMOUS_PRINCIPAL,
        credentials: Optional[Credentials] = None,
        properties: Optional[Dict[str, str]] = None,
    ):
        if credentials is None:
            credentials = Credentials()
        self._internal = InternalSession(Connection(url, principal, credentials))
        if properties is None:
            properties = {}
        self.properties = properties

    async def __aenter__(self):
        try:
            await self.connect()
        except DiffusionError as ex:
            await self.close()
            sys.exit(ex)
        else:
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self, properties: Optional[Dict[str, str]] = None):
        """ Connect to the server.

            Args:
                properties: A dict of Diffusion session properties to set and/or
                            update at connection.
        """
        if properties is not None:
            self.properties.update(properties)
        await self._internal.connect(self.properties)

    async def close(self):
        """ Closes the session. """
        await self._internal.close()

    @property
    def state(self):
        """ Returns the current connection state of the session. """
        return self._internal.connection.state

    @property
    def session_id(self):
        """ The current session ID. """
        return self._internal.session_id

    @property
    def services(self):
        """ The ServiceLocator instance responsible for retrieving services. """
        return self._internal.services

    @property
    def data(self) -> dict:
        """ Internal data storage. """
        return self._internal.data

    async def ping_server(self):
        """ Send the user ping to the server. """
        return await self._internal.send_request(self.services.USER_PING)

    def _add_ping_handler(self, callback: Callable) -> None:
        """ Register a new handler for system pings.

            Args:
                callback: The callable to be executed when a system ping message
                          is received by the session.
        """
        service_type = cast(Hashable, type(self.services.SYSTEM_PING))
        self._internal.handlers[service_type] = callback

    async def _set_principal(self, new_principal: str) -> None:
        """ Update the security principal associated with the session. """
        service = self.services.CHANGE_PRINCIPAL
        service.request.set(new_principal, self._internal.connection.credentials.password)
        response = await self._internal.send_request(service)
        if response["boolean"]:
            self._internal.connection.principal = new_principal
