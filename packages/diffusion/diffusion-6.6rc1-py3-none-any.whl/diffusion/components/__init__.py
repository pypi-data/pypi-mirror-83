""" Base features module."""

from diffusion.session import Session


class Component:
    """ A base class for various Diffusion "components".

        Args:
            session: The active `Session` to operate on.
    """

    def __init__(self, session: Session):
        self.session = session._internal
        self.services = self.session.services
