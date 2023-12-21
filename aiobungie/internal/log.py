# MIT License
#
# Copyright (c) 2020 - Present nxtlo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

__all__ = ("alloc", "TRACE", "jsonify", "init", "DEBUG")

import importlib.util
import logging
import pathlib
import sys
import typing

from aiobungie import error as _error
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    from typing_extensions import NotRequired
    from typing_extensions import Required
    from typing_extensions import Unpack

    from aiobungie import typedefs

TRACE: typing.Final[int] = logging.DEBUG - 5
"""The trace logging level for the `RESTClient` responses.

You can enable this with the following code

>>> import logging
>>> logging.getLogger("aiobungie.rest").setLevel(aiobungie.log.TRACE)
# or
>>> logging.basicConfig(level=aiobungie.log.TRACE)
# Or
>>> client = aiobungie.RESTClient(..., enable_debug="TRACE")
# Or if you're using `aiobungie.Client`
>>> client = aiobungie.Client(...)
>>> client.rest.enable_debugging(level=aiobungie.log.TRACE, file="rest_logs.txt") # optional file
"""
DEBUG = logging.DEBUG

logging.addLevelName(TRACE, "TRACE")


def _rich_enabled() -> bool:
    return importlib.util.find_spec("rich") is not None


class _Settings(typing.TypedDict, total=False):
    name: Required[str]
    no_color: NotRequired[bool]
    level: NotRequired[int | bool | typing.Literal["TRACE"]]
    file: NotRequired[str | pathlib.Path | None]


def init(
    file: str | pathlib.Path | None = None,
    level: int | bool | typing.Literal["TRACE"] | None = None,
) -> None:
    file_handler = logging.FileHandler(file, mode="w") if file else None
    handlers = [file_handler] if file_handler else None
    format = "%(levelname)-1.1s " "%(asctime)23.23s " "%(name)s: " "%(message)s"

    if level == "TRACE" or level == TRACE:
        logging.basicConfig(
            level=TRACE,
            handlers=handlers,
            format=format,
            stream=sys.stdout,
        )

    elif level is True:
        logging.basicConfig(
            level=logging.DEBUG,
        )


def alloc(**settings: Unpack[_Settings]) -> logging.Logger:
    """Allocate an aiobungie global logger.

    Parameters
    ----------
    name: `Required[str]`
        The name of the logger.
    level: `NotRequired[int | bool | typing.Literal["TRACE"] | None]`
        The level of the logger. This field is not required.

    Logging Levels
    --------------
    * `False`: This will disable logging.
    * `True`: This will set the level to `DEBUG` and enable logging minimal information.
    * `"TRACE" | aiobungie.TRACE`: This will log the response headers along with the minimal information.

    no_color: `NotRequired[bool]`
        Whether to log with colors or not. Defaults to `True`.
        This field is not required.
    file: `NotRequired[str | pathlib.Path]`
        An optional path to write the logs into. This field is not required.

    Returns
    -------
    `logging.Logger`
        The allocated logger.
    """
    logger = logging.getLogger(settings["name"])
    logging.logThreads = False
    logging.logMultiprocessing = False
    logging.logProcesses = False
    logging.captureWarnings(True)

    init(settings.get("file"), settings.get("level"))
    if _rich_enabled():
        logger.info("Rich enabled.")
        import rich.console
        import rich.logging

        console = rich.console.Console(no_color=settings.get("no_color"))
        logger.propagate = False
        logger.addHandler(
            rich.logging.RichHandler(rich_tracebacks=True, console=console)
        )
        print("LOGGED AS RICH")

    return logger


def jsonify(
    logger: logging.Logger,
    data: typedefs.JSONObject | str,
    level: int = logging.DEBUG,
) -> None:
    """Log the output as a pretty JSON string

    Parameters
    ----------
    logger: `logging.Logger`
        An instance of a logger.
    data: `aiobungie.typedefs.JSONObject`
        The JSON like object.

    """
    if _rich_enabled():
        logger.info("Rich enabled.")
        import rich.highlighter
        import rich.json

        if not isinstance(data, str):
            data = helpers.dumps(data).decode("utf-8")

        logger.log(
            level,
            rich.json.JSON(data).text,
            extra={"highlighter": rich.highlighter.JSONHighlighter()},
        )
        print("LOGGED AS RICH")
    else:
        logger.log(level, _error.stringify_http_message(data))
