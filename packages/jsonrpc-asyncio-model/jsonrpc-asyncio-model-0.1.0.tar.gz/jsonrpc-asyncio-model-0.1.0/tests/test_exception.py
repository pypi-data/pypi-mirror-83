"""
Tests for JSON-RPC exceptions.
"""

import pytest

from jsonrpc.model import (
    JsonRpcException,
    ParseError,
    InvalidRequest,
    MethodNotFound,
    InvalidParams,
    InternalError,
    ServerError,
    MethodExecutionError
)


def test_exception_with_data():
    with pytest.raises(JsonRpcException) as excinfo:
        raise JsonRpcException([1, 2, 3], 100, "message")
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.data == [1, 2, 3]
    assert excinfo.value.code == 100
    assert excinfo.value.message == "message"


def test_exception_no_data():
    with pytest.raises(JsonRpcException) as excinfo:
        raise JsonRpcException(code = 100, message = "message")
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.data == None
    assert excinfo.value.code == 100
    assert excinfo.value.message == "message"


def test_exception_no_code():
    with pytest.raises(ValueError):
        raise JsonRpcException(message = "message")


def test_exception_no_message():
    with pytest.raises(ValueError):
        raise JsonRpcException(code = 100)


def test_exception_str():
    exc = JsonRpcException(code = 100, message = "message", data = [1, 2, 3])
    assert str(exc) == "message"


def test_exception_repr():
    exc = JsonRpcException(code = 100, message = "message", data = [1, 2, 3])
    assert repr(exc) == "JsonRpcException('message', code = 100)"


def test_parse_error():
    with pytest.raises(ParseError) as excinfo:
        raise ParseError()
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.code == -32700
    assert excinfo.value.message == "Parse error"


def test_invalid_request():
    with pytest.raises(InvalidRequest) as excinfo:
        raise InvalidRequest()
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.code == -32600
    assert excinfo.value.message == "Invalid request"


def test_method_not_found():
    with pytest.raises(MethodNotFound) as excinfo:
        raise MethodNotFound()
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.code == -32601
    assert excinfo.value.message == "Method not found"


def test_invalid_params():
    with pytest.raises(InvalidParams) as excinfo:
        raise InvalidParams()
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.code == -32602
    assert excinfo.value.message == "Invalid params"


def test_internal_error():
    with pytest.raises(InternalError) as excinfo:
        raise InternalError()
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.code == -32603
    assert excinfo.value.message == "Internal error"


def test_server_error():
    with pytest.raises(ServerError) as excinfo:
        raise ServerError()
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.code == -32000
    assert excinfo.value.message == "Server error"


def test_method_execution_error():
    with pytest.raises(MethodExecutionError) as excinfo:
        try:
            {}['invalid_key']
        except KeyError as exc:
            raise MethodExecutionError.from_exception(exc)
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.code == -32099
    assert excinfo.value.message == "Key error"
    assert excinfo.value.data == "'invalid_key'"


def test_custom_error():
    class CustomError(JsonRpcException):
        code = 1000
        message = "Custom error message"
    with pytest.raises(CustomError) as excinfo:
        raise CustomError([1, 2, 3])
    assert issubclass(excinfo.type, JsonRpcException)
    assert excinfo.value.code == 1000
    assert excinfo.value.message == "Custom error message"
    assert excinfo.value.data == [1, 2, 3]
