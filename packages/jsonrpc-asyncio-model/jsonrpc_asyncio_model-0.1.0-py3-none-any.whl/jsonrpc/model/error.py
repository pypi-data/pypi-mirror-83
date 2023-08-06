"""
Models describing JSON-RPC errors.
"""

from typing import Any

from pydantic import BaseModel, Extra, StrictInt, constr

from .exceptions import JsonRpcException


class Error(BaseModel):
    """
    Model for a JSON-RPC error.
    """
    class Config:
        # Using orm_mode allows the creation of errors from exceptions
        orm_mode = True
        extra = Extra.forbid

    #: The error code
    code: StrictInt
    #: The error message
    message: constr(min_length = 1, strict = True)
    #: Additional information about the error
    data: Any = None

    def exception(self):
        """
        Returns a JSON-RPC exception for this error.
        """
        return JsonRpcException(self.data, self.code, self.message)
