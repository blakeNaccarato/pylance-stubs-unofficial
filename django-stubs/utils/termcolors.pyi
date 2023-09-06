from collections.abc import Callable, Sequence
from typing import Any

color_names: Any
foreground: Any
background: Any
RESET: str
opt_dict: Any

def colorize(
    text: str | None = ..., opts: Sequence[str] = ..., **kwargs: Any
) -> str: ...
def make_style(opts: tuple[Any, ...] = ..., **kwargs: Any) -> Callable[..., Any]: ...

NOCOLOR_PALETTE: str
DARK_PALETTE: str
LIGHT_PALETTE: str
PALETTES: Any
DEFAULT_PALETTE: str = ...

def parse_color_setting(
    config_string: str,
) -> dict[str, dict[str, tuple[str] | str]] | None: ...
