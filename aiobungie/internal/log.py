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

__all__ = ("TRACE", "jsonify", "init", "DEBUG")

import importlib.util
import logging
import sys
import typing

from aiobungie import error as _error
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
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


def init(
    logger: logging.Logger, level: typing.Literal["TRACE"] | bool | int = False
) -> None:
    """Allocate an aiobungie global logger.

    Parameters
    ----------
    level: `NotRequired[int | bool | typing.Literal["TRACE"] | None]`
        The level of the logger. This field is not required.

    Logging Levels
    --------------
    * `False`: This will disable logging.
    * `True`: This will set the level to `DEBUG` and enable logging minimal information.
    * `"TRACE" | aiobungie.TRACE`: This will log the response headers along with the minimal information.
    """
    logging.logThreads = False
    logging.logMultiprocessing = False
    logging.logProcesses = False
    logging.captureWarnings(True)

    format = "%(levelname)s " "%(asctime)23.23s " "%(name)s: " "%(message)s"

    if level == "TRACE" or level == TRACE:
        logger.setLevel(TRACE)
        logging.basicConfig(
            level=TRACE,
            format=format,
            stream=sys.stdout,
        )

    elif level is True:
        logger.setLevel(DEBUG)
        logging.basicConfig(
            level=logging.DEBUG,
            format=format,
            stream=sys.stdout,
        )

    if _rich_enabled():
        import rich.console
        import rich.logging
        import rich.traceback

        logger.addHandler(rich.logging.RichHandler(rich_tracebacks=True))

        rich.traceback.install()


def jsonify(
    logger: logging.Logger,
    data: typedefs.JSONArray | typedefs.JSONObject | str,
    level: int = logging.DEBUG,
) -> None:
    """Log the output as a pretty JSON string

    Parameters
    ----------
    logger: `logging.Logger`
        An instance of a logger.
    data: `typedefs.JSONObject | typedefs.JSONArray | str`
        The JSON like object. If the object is a string, it will be dumped to a JSON string.
    """
    if _rich_enabled():
        import rich.highlighter
        import rich.json

        if not isinstance(data, str):
            # rich needs the object to be a string.
            data = helpers.dumps(data).decode("utf-8")

        logger.log(
            level,
            rich.json.JSON(data).text,
            extra={"highlighter": rich.highlighter.JSONHighlighter()},
        )
    else:
        logger.log(
            level, _error.stringify_headers(data) if isinstance(data, dict) else data
        )
