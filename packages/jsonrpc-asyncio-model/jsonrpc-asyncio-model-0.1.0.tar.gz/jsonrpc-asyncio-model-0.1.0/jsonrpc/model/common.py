"""
Common types shared by request and response.
"""

from typing import Union
from typing_extensions import Literal

from pydantic import StrictInt, constr


#: The JSON-RPC version as a string
JSONRPC_VERSION = "2.0"

#: Type-alias for the JSON-RPC version
Version = Literal[JSONRPC_VERSION]

#: Type-alias for a valid id
Id = Union[constr(min_length = 1, strict = True), StrictInt]
