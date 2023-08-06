""" Messaging handlers. """

from typing import Callable

from diffusion import datatypes as dt
from diffusion.internal import utils


class MessagingRequestHandler:
    """ Handler for messaging requests. """

    def __init__(
        self,
        callback: Callable,
        request_type: dt.DataTypeArgument,
        response_type: dt.DataTypeArgument,
    ):
        self.request_type = dt.get(request_type)
        self.response_type = dt.get(response_type)
        self.callback = utils.coroutine(callback)

    async def __call__(self, request: dt.DataType, context=None) -> dt.DataType:
        """ Execute the callback. """
        if type(request) is not self.request_type:
            raise dt.IncompatibleDatatypeError(
                "Incompatible request data type: "
                f"required: {self.request_type.__name__}; submitted: {type(request).__name__}"
            )
        response = await self.callback(request.value, context)
        try:
            response = self.response_type(response)
        except dt.DataTypeError as ex:
            raise dt.IncompatibleDatatypeError from ex
        return response
