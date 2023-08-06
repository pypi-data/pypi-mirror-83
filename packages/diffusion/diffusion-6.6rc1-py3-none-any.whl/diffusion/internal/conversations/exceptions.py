""" Conversation errors. """

from diffusion.internal.exceptions import DiffusionError


class ConversationError(DiffusionError):
    """ Base conversation error. """


class CIDGeneratorExhaustedError(ConversationError):
    """ Error stating that a CID generator was exhausted. """


class NoSuchConversationError(ConversationError):
    """ The conversation with this CID does not exist in the `ConversationSet`. """

    def __init__(self, cid):
        super().__init__(f"Unknown conversation {cid}")


class ConversationFinished(ConversationError):
    """ Conversation has been completed. """
