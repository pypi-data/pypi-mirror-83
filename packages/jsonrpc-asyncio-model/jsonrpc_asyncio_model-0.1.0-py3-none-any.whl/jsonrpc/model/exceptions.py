"""
Module containing JSON-RPC exceptions.
"""

import re


class JsonRpcException(RuntimeError):
    """
    Base class for all JSON-RPC exceptions.
    """
    code = None
    message = None

    def __init_subclass__(cls):
        # If no default message is set, set a default one based on the class name
        if not cls.message:
            # Split the class name into words
            words = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', cls.__name__)
            # Recombine and capitalise
            cls.message = ' '.join(words).lower().capitalize()

    def __init__(self, data = None, code = None, message = None):
        self.data = data
        self.code = code or self.code
        if self.code is None:
            raise ValueError('code is not given and has no default')
        self.message = message or self.message
        if self.message is None:
            raise ValueError('message is not given and has no default')

    def __str__(self):
        return self.message

    def __repr__(self):
        return "JsonRpcException({}, code = {})".format(repr(self.message), self.code)


class ParseError(JsonRpcException):
    """
    Raised when a parse error occurs.
    """
    code = -32700


class InvalidRequest(JsonRpcException):
    """
    Raised for an invalid request.
    """
    code = -32600


class MethodNotFound(JsonRpcException):
    """
    Raised when a method does not exist or is not available.
    """
    code = -32601


class InvalidParams(JsonRpcException):
    """
    Raised when invalid parameters are given.
    """
    code = -32602


class InternalError(JsonRpcException):
    """
    Raised when an internal JSON-RPC error occurs.
    """
    code = -32603


class ServerError(JsonRpcException):
    """
    Raised when a server error occurs.
    """
    code = -32000


class MethodExecutionError(JsonRpcException):
    """
    Raised when an exception occurs during method execution.
    """
    code = -32099

    @classmethod
    def from_exception(cls, exc):
        """
        Returns a method execution error for the given exception.
        """
        # Convert the exception name to words for the message
        words = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', exc.__class__.__name__)
        # Recombine and capitalise
        message = ' '.join(words).lower().capitalize()
        return cls(data = str(exc), message = message)
