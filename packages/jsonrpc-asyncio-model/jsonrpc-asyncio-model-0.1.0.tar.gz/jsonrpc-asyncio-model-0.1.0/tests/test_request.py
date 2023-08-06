"""
Tests for the JSON-RPC models.
"""

import functools
import json
import uuid

import pytest

from pydantic import ValidationError

from jsonrpc.model import Request, BatchRequest

from .util import raises_validation_error


class AnyUuid:
    """
    Class that compares as equal to any UUID.

    Used when comparing generated request ids where we don't care what the
    id is - only that it is there and is a UUID.
    """
    def __eq__(self, other):
        if isinstance(other, uuid.UUID):
            return True
        # Try to create a UUID object from the string
        try:
            id = uuid.UUID(other)
        except ValueError:
            return False
        else:
            return True


def test_request_version_valid():
    request = Request(jsonrpc = "2.0", method = "method")
    assert request.jsonrpc == "2.0"


@raises_validation_error(('jsonrpc', 'value_error.missing'))
def test_request_version_missing():
    request = Request(method = "method")


@raises_validation_error(('jsonrpc', 'value_error.const'))
def test_request_version_invalid_type():
    request = Request(jsonrpc = 10, method = 'method')


@raises_validation_error(('jsonrpc', 'value_error.const'))
def test_request_version_invalid_value():
    request = Request(jsonrpc = "2.1", method = "method")


def test_request_id_string():
    request = Request(
        jsonrpc = "2.0",
        method = "method",
        id = "1e666df7-c0c6-4d13-a60c-87d216cf1090"
    )
    assert request.id == "1e666df7-c0c6-4d13-a60c-87d216cf1090"


def test_request_id_integer():
    request = Request(jsonrpc = "2.0", method = "method", id = 10)
    assert request.id == 10


def test_request_id_null():
    request = Request(jsonrpc = "2.0", method = "method", id = None)
    assert request.id is None


def test_request_id_not_given():
    request = Request(jsonrpc = "2.0", method = "method")
    assert request.id is None


def test_request_id_no_coerce():
    # Test that strings that look like integers are not coerced
    request = Request(jsonrpc = "2.0", method = "method", id = '1')
    assert request.id == '1'


@raises_validation_error(('id', 'type_error.str'), ('id', 'type_error.integer'))
def test_request_id_invalid_type():
    request = Request(jsonrpc = "2.0", method = "method", id = 1.0)


@raises_validation_error(('id', 'value_error.any_str.min_length'), ('id', 'type_error.integer'))
def test_request_id_empty_string():
    request = Request(jsonrpc = "2.0", method = "method", id = "")


def test_request_method_valid():
    request = Request(jsonrpc = "2.0", method = "method")
    assert request.method == "method"


@raises_validation_error(('method', 'value_error.missing'))
def test_request_method_missing():
    request = Request(jsonrpc = "2.0")


@raises_validation_error(('method', 'type_error.str'))
def test_request_method_invalid_type():
    request = Request(jsonrpc = "2.0", method = 10)


@raises_validation_error(('method', 'value_error.any_str.min_length'))
def test_request_method_empty_string():
    request = Request(jsonrpc = "2.0", method = "")


def test_request_params_positional():
    request = Request(jsonrpc = "2.0", method = "method", params = [1, 2, 3])
    assert request.params == [1, 2, 3]


def test_request_params_keyword():
    request = Request(jsonrpc = "2.0", method = "method", params = {"a": 1, "b": 2})
    assert request.params == {"a": 1, "b": 2}


def test_request_params_not_given():
    request = Request(jsonrpc = "2.0", method = "method")
    assert request.params == {}


@raises_validation_error(('params', 'type_error.list'), ('params', 'type_error.dict'))
def test_request_params_invalid_type():
    request = Request(jsonrpc = "2.0", method = "method", params = 10)


@raises_validation_error(('params', 'type_error.list'), (('params', '__key__'), 'type_error.str'))
def test_request_params_invalid_dict_keys():
    request = Request(jsonrpc = "2.0", method = "method", params = {1: 2, 3: 4})


@raises_validation_error(('unknown', 'value_error.extra'))
def test_request_unknown_key_forbidden():
    request = Request(jsonrpc = "2.0", method = "method", unknown = 10)


def test_request_create_positional_args():
    request = Request.create("method", 1, 2, 3)
    assert request.id == AnyUuid()
    assert request.method == "method"
    assert request.params == [1, 2, 3]


def test_request_create_keyword_args():
    request = Request.create("method", a = 1, b = 2, c = 3)
    assert request.id == AnyUuid()
    assert request.method == "method"
    assert request.params == {"a": 1, "b": 2, "c": 3}


def test_request_create_no_args():
    request = Request.create("method")
    assert request.id == AnyUuid()
    assert request.method == "method"
    assert request.params == {}


def test_request_create_notification():
    request = Request.create("method", 1, 2, 3, _notification = True)
    assert request.id is None
    assert request.method == "method"
    assert request.params == [1, 2, 3]


def test_request_create_position_keyword_mutually_exclusive():
    with pytest.raises(ValueError):
        request = Request.create("method", 1, 2, c = 3)


def test_request_to_json_positional_params():
    request = Request(jsonrpc = "2.0", method = "method", id = 10, params = [1, 2, 3])
    expected = dict(jsonrpc = "2.0", method = "method", id = 10, params = [1, 2, 3])
    assert json.loads(request.json()) == expected


def test_request_to_json_keyword_args():
    request = Request(jsonrpc = "2.0", method = "method", id = 10, params = {"a": 1, "b": 2})
    expected = dict(jsonrpc = "2.0", method = "method", id = 10, params = {"a": 1, "b": 2})
    assert json.loads(request.json()) == expected


def test_request_to_json_no_params():
    request = Request(jsonrpc = "2.0", method = "method", id = 10)
    expected = dict(jsonrpc = "2.0", method = "method", id = 10)
    assert json.loads(request.json()) == expected


def test_request_to_json_null_id():
    request = Request(jsonrpc = "2.0", method = "method", id = None)
    expected = dict(jsonrpc = "2.0", method = "method", id = None)
    assert json.loads(request.json()) == expected


def test_request_to_json_no_id():
    request = Request(jsonrpc = "2.0", method = "method")
    expected = dict(jsonrpc = "2.0", method = "method")
    assert json.loads(request.json()) == expected


def test_batch_request_valid_requests():
    req1 = Request(jsonrpc = "2.0", method = "method")
    req2 = Request(jsonrpc = "2.0", method = "method2")
    request = BatchRequest.parse_obj([req1, req2])
    assert len(request) == 2
    assert list(request) == [req1, req2]
    assert next(iter(request)).method == "method"


@raises_validation_error((('__root__', 1), 'type_error.dict'))
def test_batch_request_not_a_request():
    req1 = Request(jsonrpc = "2.0", method = "method")
    request = BatchRequest.parse_obj([req1, 10])


@raises_validation_error(('__root__', 'value_error.list.min_items'))
def test_batch_request_empty():
    request = BatchRequest.parse_obj([])


@raises_validation_error(('__root__', 'type_error.list'))
def test_batch_request_not_list():
    request = BatchRequest.parse_obj(10)


def test_batch_request_create_valid():
    req1 = Request(jsonrpc = "2.0", method = "method")
    req2 = Request(jsonrpc = "2.0", method = "method2")
    request = BatchRequest.create(req1, req2)
    assert len(request) == 2
    assert list(request) == [req1, req2]
    assert next(iter(request)).method == "method"


@raises_validation_error(('__root__', 'value_error.list.min_items'))
def test_batch_request_create_empty():
    request = BatchRequest.create()


def test_batch_request_to_json_positional_params():
    request = BatchRequest.create(
        Request(jsonrpc = "2.0", method = "method", id = 10, params = [1, 2, 3])
    )
    expected = [dict(jsonrpc = "2.0", method = "method", id = 10, params = [1, 2, 3])]
    assert json.loads(request.json()) == expected


def test_batch_request_to_json_keyword_args():
    request = BatchRequest.create(
        Request(jsonrpc = "2.0", method = "method", id = 10, params = {"a": 1, "b": 2})
    )
    expected = [dict(jsonrpc = "2.0", method = "method", id = 10, params = {"a": 1, "b": 2})]
    assert json.loads(request.json()) == expected


def test_batch_request_to_json_no_params():
    request = BatchRequest.create(
        Request(jsonrpc = "2.0", method = "method", id = 10)
    )
    expected = [dict(jsonrpc = "2.0", method = "method", id = 10)]
    assert json.loads(request.json()) == expected


def test_batch_request_to_json_null_id():
    request = BatchRequest.create(
        Request(jsonrpc = "2.0", method = "method", id = None)
    )
    expected = [dict(jsonrpc = "2.0", method = "method", id = None)]
    assert json.loads(request.json()) == expected


def test_batch_request_to_json_no_id():
    request = BatchRequest.create(
        Request(jsonrpc = "2.0", method = "method")
    )
    expected = [dict(jsonrpc = "2.0", method = "method")]
    assert json.loads(request.json()) == expected


def test_batch_request_to_json_multiple():
    request = BatchRequest.create(
        Request(jsonrpc = "2.0", method = "method", id = 10),
        Request(jsonrpc = "2.0", method = "method", id = 11)
    )
    expected = [
        dict(jsonrpc = "2.0", method = "method", id = 10),
        dict(jsonrpc = "2.0", method = "method", id = 11)
    ]
    assert json.loads(request.json()) == expected
