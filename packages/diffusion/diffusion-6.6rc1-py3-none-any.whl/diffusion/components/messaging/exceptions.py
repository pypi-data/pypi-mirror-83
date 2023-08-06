""" Messaging-specific exception classes. """

from diffusion.internal.exceptions import DiffusionError


class MessagingError(DiffusionError):
    """ The generic messaging error. """
