"""
Utilities for the JSON-RPC model tests.
"""

import contextlib

import pytest

from pydantic import ValidationError


@contextlib.contextmanager
def raises_validation_error(*args):
    """
    Context manager that ensures the wrapped code raises a Pydantic validation
    error where the expected errors occur.

    Each expected error is a tuple of location and type. The location can be either
    a string or a tuple for nested validation.
    """
    with pytest.raises(ValidationError) as excinfo:
        yield
    # Index the expected error types by location
    expected = {}
    for loc, et in args:
        if not isinstance(loc, tuple):
            loc = (loc, )
        expected.setdefault(loc, set()).add(et)
    found = {}
    for error in excinfo.value.errors():
        found.setdefault(error['loc'], set()).add(error['type'])
    assert found == expected


def compare_validation_error(excinfo, *args):
    """
    Context manager that ensures the wrapped code raises a Pydantic validation
    error where the expected errors occur.

    Each expected error is a tuple of location and type. The location can be either
    a string or a tuple for nested validation.
    """
    # Index the expected error types by location
    expected = {}
    for loc, et in args:
        if not isinstance(loc, tuple):
            loc = (loc, )
        expected.setdefault(loc, set()).add(et)
    found = {}
    for error in excinfo.value.errors():
        found.setdefault(error['loc'], set()).add(error['type'])
    assert found == expected