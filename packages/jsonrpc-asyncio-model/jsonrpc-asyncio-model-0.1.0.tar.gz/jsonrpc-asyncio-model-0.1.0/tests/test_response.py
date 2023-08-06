"""
Tests for the JSON-RPC models.
"""

import contextlib
import functools
import json

import pytest

from pydantic import ValidationError

from jsonrpc.model import Response, BatchResponse, Error, JsonRpcException

from .util import raises_validation_error


def test_response_version_valid():
    response = Response(jsonrpc = "2.0", result = 10, id = 10)
    assert response.jsonrpc == "2.0"


@raises_validation_error(('jsonrpc', 'value_error.missing'))
def test_response_version_missing():
    response = Response(result = 10, id = 10)


@raises_validation_error(('jsonrpc', 'value_error.const'))
def test_response_version_invalid_type():
    response = Response(jsonrpc = 10, result = 10, id = 10)


@raises_validation_error(('jsonrpc', 'value_error.const'))
def test_response_version_invalid_value():
    response = Response(jsonrpc = "2.1", result = 10, id = 10)


def test_response_id_string():
    response = Response(
        jsonrpc = "2.0",
        result = 10,
        id = "1e666df7-c0c6-4d13-a60c-87d216cf1090"
    )
    assert response.id == "1e666df7-c0c6-4d13-a60c-87d216cf1090"


def test_response_id_integer():
    response = Response(jsonrpc = "2.0", result = 10, id = 10)
    assert response.id == 10


def test_response_id_null():
    # Null id is only permitted for error responses
    # Success responses with null id are notifications and shouldn't be emitting responses
    response = Response(jsonrpc = "2.0", error = dict(code = 100, message = "message"), id = None)
    assert response.id is None
    with raises_validation_error(('__root__', 'value_error')):
        response = Response(jsonrpc = "2.0", result = 10, id = None)


def test_response_id_no_coerce():
    # Test that strings that look like integers are not coerced
    response = Response(jsonrpc = "2.0", result = 10, id = '1')
    assert response.id == '1'


@raises_validation_error(('id', 'value_error.missing'))
def test_response_id_not_given():
    response = Response(jsonrpc = "2.0", result = 10)


@raises_validation_error(('id', 'type_error.str'), ('id', 'type_error.integer'))
def test_response_id_invalid_type():
    response = Response(jsonrpc = "2.0", result = 10, id = 1.0)


@raises_validation_error(('id', 'value_error.any_str.min_length'), ('id', 'type_error.integer'))
def test_response_id_empty_string():
    response = Response(jsonrpc = "2.0", result = 10, id = "")


def test_response_result_valid():
    # Test a variety of response types that should be valid
    make = functools.partial(Response, jsonrpc = "2.0", id = 10)
    # Test a variety of different result types
    response = make(result = 10)
    assert response.result == 10
    assert response.error is None
    response = make(result = "10 items")
    assert response.result == "10 items"
    assert response.error is None
    response = make(result = [1, 2.0, "3"])
    assert response.result == [1, 2.0, "3"]
    assert response.error is None
    response = make(result = {"a": 1, 2: 3.0})
    assert response.result == {"a": 1, 2: 3.0}
    assert response.error is None
    response = make(result = None)
    assert response.result is None
    assert response.error is None


def test_response_valid_error():
    make = functools.partial(Response, jsonrpc = "2.0", id = 10)
    # With an error object
    response = make(error = Error(code = 100, message = "message"))
    assert isinstance(response.error, Error)
    assert response.error.code == 100
    assert response.error.message == "message"
    # Error data as a dict
    response = make(error = dict(code = 100, message = "message"))
    assert isinstance(response.error, Error)
    assert response.error.code == 100
    assert response.error.message == "message"
    # Error data from an exception
    exception = JsonRpcException(code = 100, message = "message")
    response = make(error = exception)
    assert isinstance(response.error, Error)
    assert response.error.code == 100
    assert response.error.message == "message"


@raises_validation_error(('error', 'assertion_error'), ('__root__', 'value_error'))
def test_response_error_null():
    response = Response(jsonrpc = "2.0", id = 10, error = None)


@raises_validation_error(('__root__', 'value_error'))
def test_response_result_and_error():
    response = Response(
        jsonrpc = "2.0",
        id = 10,
        result = 10,
        error = Error(code = 100, message = "message")
    )


@raises_validation_error(('__root__', 'value_error'))
def test_response_result_error_missing():
    response = Response(jsonrpc = "2.0", id = 10)


@raises_validation_error(('unknown', 'value_error.extra'))
def test_response_unknown_key_forbidden():
    response = Response(jsonrpc = "2.0", result = 10, id = 10, unknown = 10)


def test_response_create_success():
    response = Response.create_success(result = 10, id = 100)
    assert response.id == 100
    assert response.result == 10


def test_response_create_error_id():
    response = Response.create_error(error = Error(code = 100, message = "message"), id = 100)
    assert response.id == 100
    assert response.error == Error(code = 100, message = "message")


def test_response_create_error_no_id():
    response = Response.create_error(error = Error(code = 100, message = "message"))
    assert response.id is None
    assert response.error == Error(code = 100, message = "message")


def test_response_to_json_success():
    response = Response(jsonrpc = "2.0", result = [1, 2, 3], id = 10)
    expected = dict(jsonrpc = "2.0", result = [1, 2, 3], id = 10)
    assert json.loads(response.json()) == expected


def test_response_to_json_error_data():
    response = Response(
        jsonrpc = "2.0",
        error = Error(code = 100, message = "message", data = [1, 2, 3]),
        id = 10
    )
    expected = dict(
        jsonrpc = "2.0",
        error = dict(code = 100, message = "message", data = [1, 2, 3]),
        id = 10
    )
    assert json.loads(response.json()) == expected


def test_response_to_json_error_no_data():
    response = Response(jsonrpc = "2.0", error = Error(code = 100, message = "message"), id = 10)
    expected = dict(jsonrpc = "2.0", error = dict(code = 100, message = "message"), id = 10)
    assert json.loads(response.json()) == expected


def test_response_to_json_id_null():
    response = Response(jsonrpc = "2.0", error = Error(code = 100, message = "message"), id = None)
    expected = dict(jsonrpc = "2.0", error = dict(code = 100, message = "message"), id = None)
    assert json.loads(response.json()) == expected


def test_batch_response_valid_responses():
    res1 = Response(jsonrpc = "2.0", result = 10, id = 10)
    res2 = Response(jsonrpc = "2.0", result = 20, id = 11)
    response = BatchResponse.parse_obj([res1, res2])
    assert len(response) == 2
    assert list(response) == [res1, res2]
    assert next(iter(response)).result == 10


@raises_validation_error((('__root__', 1, 'jsonrpc'), 'value_error.missing'))
def test_batch_response_not_a_response():
    response = BatchResponse.parse_obj([
        Response(jsonrpc = "2.0", result = 10, id = 10),
        dict(result = 10, id = 11)
    ])


@raises_validation_error(('__root__', 'value_error.list.min_items'))
def test_batch_response_empty():
    response = BatchResponse.parse_obj([])


@raises_validation_error(('__root__', 'type_error.list'))
def test_batch_response_not_list():
    response = BatchResponse.parse_obj(10)


def test_batch_response_create_valid():
    res1 = Response(jsonrpc = "2.0", result = 10, id = 10)
    res2 = Response(jsonrpc = "2.0", result = 20, id = 11)
    response = BatchResponse.create(res1, res2)
    assert len(response) == 2
    assert list(response) == [res1, res2]
    assert next(iter(response)).result == 10


@raises_validation_error(('__root__', 'value_error.list.min_items'))
def test_batch_response_create_empty():
    response = BatchResponse.create()


def test_batch_response_to_json_success():
    response = BatchResponse.create(
        Response(jsonrpc = "2.0", result = [1, 2, 3], id = 10)
    )
    expected = [dict(jsonrpc = "2.0", result = [1, 2, 3], id = 10)]
    assert json.loads(response.json()) == expected


def test_batch_response_to_json_error_data():
    response = BatchResponse.create(
        Response(
            jsonrpc = "2.0",
            error = Error(code = 100, message = "message", data = [1, 2, 3]),
            id = 10
        )
    )
    expected = [
        dict(
            jsonrpc = "2.0",
            error = dict(code = 100, message = "message", data = [1, 2, 3]),
            id = 10
        )
    ]
    assert json.loads(response.json()) == expected


def test_batch_response_to_json_error_no_data():
    response = BatchResponse.create(
        Response(jsonrpc = "2.0", error = Error(code = 100, message = "message"), id = 10)
    )
    expected = [dict(jsonrpc = "2.0", error = dict(code = 100, message = "message"), id = 10)]
    assert json.loads(response.json()) == expected


def test_batch_response_to_json_id_null():
    response = BatchResponse.create(
        Response(jsonrpc = "2.0", error = Error(code = 100, message = "message"), id = None)
    )
    expected = [dict(jsonrpc = "2.0", error = dict(code = 100, message = "message"), id = None)]
    assert json.loads(response.json()) == expected


def test_batch_response_multiple():
    response = BatchResponse.create(
        Response(jsonrpc = "2.0", result = [1, 2, 3], id = 10),
        Response(jsonrpc = "2.0", error = Error(code = 100, message = "message"), id = 11)
    )
    expected = [
        dict(jsonrpc = "2.0", result = [1, 2, 3], id = 10),
        dict(jsonrpc = "2.0", error = dict(code = 100, message = "message"), id = 11)
    ]
    assert json.loads(response.json()) == expected
