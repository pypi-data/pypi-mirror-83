"""
Models describing the JSON-RPC request and batch request.
"""

import uuid

from typing import Any, List, Dict, Union, Optional

from pydantic import BaseModel, Extra, Field, constr, conlist

from .common import JSONRPC_VERSION, Version, Id


#: Type-alias for request parameters
Params = Union[List[Any], Dict[constr(min_length = 1, strict = True), Any]]


class Request(BaseModel):
    """
    Model for a JSON-RPC request.
    """
    class Config:
        extra = Extra.forbid

    #: The JSON-RPC version
    jsonrpc: Version
    #: The id of the request
    #: If no id is given or the given id is null, the request is a notification
    id: Optional[Id] = None
    #: The method to invoke
    method: constr(min_length = 1, strict = True)
    #: The parameters for the method invocation
    #: Parameters can be either a list for positional args or a dict for keyword args
    params: Params = Field(default_factory = dict)

    def json(self, **kwargs):
        # By default, exclude all items that were not explicitly set
        kwargs.setdefault('exclude_unset', True)
        return super().json(**kwargs)

    @classmethod
    def create(cls, method: str, *args: Any, _notification: bool = False, **kwargs: Any) -> 'Request':
        """
        Return a JSON-RPC request for the given method and arguments.
        """
        # The params can be *either* positional or keyword
        if args and kwargs:
            raise ValueError('Positional and keyword arguments are mutually exclusive.')
        request_kwargs = dict()
        # Unless we are a notification, generate an id
        if not _notification:
            request_kwargs.update(id = str(uuid.uuid4()))
        # Only include params if they are given
        if args or kwargs:
            request_kwargs.update(params = args or kwargs)
        return cls(jsonrpc = JSONRPC_VERSION, method = method, **request_kwargs)


class BatchRequest(BaseModel):
    """
    Model for a JSON-RPC batch request.
    """
    class Config:
        extra = Extra.forbid

    #: A batch request is a non-empty list of JSON-RPC requests
    __root__: conlist(Request, min_items = 1)

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def json(self, **kwargs):
        # By default, exclude all items that were not explicitly set
        kwargs.setdefault('exclude_unset', True)
        return super().json(**kwargs)

    @classmethod
    def create(cls, *requests: Request) -> 'BatchRequest':
        """
        Return a JSON-RPC batch request for the given requests.
        """
        return cls(__root__ = requests)
