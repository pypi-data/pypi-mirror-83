"""
Models describing the JSON-RPC response and batch response.
"""

from typing import Any, Optional

from pydantic import BaseModel, Extra, Field, conlist, validator, root_validator

from .common import JSONRPC_VERSION, Version, Id
from .error import Error


class _NotGiven:
    """
    Class for objects that represent a not-present value.
    """


class Response(BaseModel):
    """
    Model for a JSON-RPC response.
    """
    class Config:
        extra = Extra.forbid

    #: The JSON-RPC version
    jsonrpc: Version
    #: The id of the corresponding request
    #: This field can be none in the case where the corresponding request is a notification
    #: or the id could not be detected, but must still be given
    id: Optional[Id] = Field(...)
    #: The result of a successful method execution
    result: Optional[Any] = Field(default_factory = _NotGiven)
    #: The error that caused a method execution to fail
    error: Optional[Error] = None

    @validator('result')
    def check_result_value(cls, v):
        # This validator only runs if a result is given
        # If a result is given, it can be anything except the NOT_PRESENT sentinel
        # This is so unlikely that we don't provide a specific error message
        assert not isinstance(v, _NotGiven)
        return v

    @validator('error')
    def check_error_value(cls, v):
        # This validator only runs if an error is given
        # If it is given, it cannot be None
        assert v is not None, 'error cannot be None'
        return v

    @root_validator
    def check_result_error(cls, values):
        """
        Check that either result or error is given but not both.
        """
        result, error = values.get('result', _NotGiven()), values.get('error')
        if isinstance(result, _NotGiven) and error is None:
            raise ValueError('either result or error is required')
        if not isinstance(result, _NotGiven) and error is not None:
            raise ValueError('result and error are mutually exclusive')
        return values

    @root_validator
    def check_result_id(cls, values):
        """
        Check that a result is not given for a notification.
        """
        if 'id' in values:
            result, id = values.get('result', _NotGiven()), values['id']
            if id is None and not isinstance(result, _NotGiven):
                raise ValueError('result cannot be given for notificaton')
            return values

    def json(self, **kwargs):
        # By default, exclude all items that were not explicitly set
        kwargs.setdefault('exclude_unset', True)
        return super().json(**kwargs)

    @classmethod
    def create_success(cls, result: Any, id: Id) -> 'Response':
        """
        Return a JSON-RPC success response for the given arguments.
        """
        return cls(jsonrpc = JSONRPC_VERSION, id = id, result = result)

    @classmethod
    def create_error(cls, error: Error, id: Optional[Id] = None) -> 'Response':
        """
        Return a JSON-RPC error response for the given arguments.
        """
        return cls(jsonrpc = JSONRPC_VERSION, id = id, error = error)


class BatchResponse(BaseModel):
    """
    Model for a JSON-RPC batch response.
    """
    class Config:
        extra = Extra.forbid

    #: A batch response is a non-empty list of JSON-RPC responses
    __root__: conlist(Response, min_items = 1)

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def json(self, **kwargs):
        # By default, exclude all items that were not explicitly set
        kwargs.setdefault('exclude_unset', True)
        return super().json(**kwargs)

    @classmethod
    def create(cls, *responses: Response) -> 'BatchResponse':
        """
        Return a JSON-RPC batch response for the given responses.
        """
        return cls(__root__ = responses)
