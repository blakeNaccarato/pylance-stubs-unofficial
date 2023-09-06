from collections.abc import Callable
from typing import Any, TypeVar

_C = TypeVar("_C", bound=Callable[..., Any])

def gzip_page(view_func: _C) -> _C: ...
