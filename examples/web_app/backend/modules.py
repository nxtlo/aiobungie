"""Module objects we use for JSON payloads requests."""

import typing

import pydantic


class PlayerModule(pydantic.BaseModel):
    name: str
    """The player name we're gonna search for."""
    type: typing.Optional[str]
    """An optional player type or platform we retrieve. Default will be all."""
