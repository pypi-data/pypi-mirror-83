"""
Tests for the JSON-RPC error models.
"""

import pytest

from jsonrpc.model import Error, JsonRpcException

from .util import raises_validation_error


def test_error_no_data():
    error = Error(code = 100, message = "message")
    assert error.code == 100
    assert error.message == "message"


def test_error_simple_data():
    error = Error(code = 100, message = "message", data = 10)
    assert error.code == 100
    assert error.message == "message"
    assert error.data == 10


def test_error_complex_data():
    error = Error(code = 100, message = "message", data = {"a": 10, "b": 20})
    assert error.code == 100
    assert error.message == "message"
    assert error.data == {"a": 10, "b": 20}


@raises_validation_error(('code', 'type_error.integer'))
def test_error_non_integer_code():
    error = Error(code = 100.0, message = "message")


@raises_validation_error(('code', 'value_error.missing'))
def test_error_missing_code():
    error = Error(message = "message")


@raises_validation_error(('message', 'type_error.str'))
def test_error_non_string_message():
    error = Error(code = 100, message = 10)


@raises_validation_error(('message', 'value_error.any_str.min_length'))
def test_error_empty_message():
    error = Error(code = 100, message = "")


@raises_validation_error(('message', 'value_error.missing'))
def test_error_missing_message():
        error = Error(code = 100)


def test_error_from_exception():
    exception = JsonRpcException(code = 100, message = "message", data = [1, 2, 3])
    error = Error.from_orm(exception)
    assert error.code == 100
    assert error.message == "message"
    assert error.data == [1, 2, 3]


def test_error_to_exception():
    error = Error(code = 100, message = "message")
    exc = error.exception()
    assert isinstance(exc, JsonRpcException)
    assert exc.code == 100
    assert exc.message == "message"
