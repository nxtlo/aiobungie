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

"""aiobungie assets module for API Image hash and path linking."""


from __future__ import annotations

__all__: tuple[str, ...] = ("Image", "MimeType")

import asyncio
import collections.abc as collections
import concurrent.futures
import logging
import pathlib
import typing

import aiohttp

from aiobungie import url

from . import enums
from . import helpers

_LOGGER: typing.Final[logging.Logger] = logging.getLogger("aiobungie.assets")


class MimeType(str, enums.Enum):
    """Image mime types enum."""

    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"
    JPG = "jpg"
    GIF = "gif"

    def __str__(self) -> str:
        return str(self.value)


def _write(
    path: pathlib.Path,
    file_name: str,
    mimetype: typing.Union[str, MimeType],
    data: bytes,
) -> None:

    with open(path.name + f"{file_name}.{mimetype}", "wb") as file:
        file.write(data)


class Image:
    """Representation of an image/avatar/picture at Bungie.

    Example
    -------
    ```py
    from aiobungie import Image
    img = Image("img/destiny_content/pgcr/raid_eclipse.jpg")
    print(img)
    # https://www.bungie.net/img/destiny_content/pgcr/raid_eclipse.jpg

    # Stream the image.
    async for chunk in img:
        # Byte chunks of the image.
        print(chunk)

    # Save the image to a file.
    await img.save("file_name", "/my/path/to/save/to", "jpeg")
    ```

    Parameters
    ----------
    path : `str | None`
        The path to the image. If `None`, the default missing image path will be used.
    """

    __slots__ = ("_path",)

    def __init__(self, path: typing.Optional[str] = None) -> None:
        self._path = path

    @property
    def is_missing(self) -> bool:
        return not self._path

    @property
    def url(self) -> str:
        """The URL to the image."""
        return self.create_url()

    @staticmethod
    def missing_path() -> str:
        """Returns the path to the missing Bungie image."""
        return "img/misc/missing_icon_d2.png"

    def create_url(self) -> str:
        """Creates a full URL to the image path.

        Returns
        -------
        str
            The URL to the image.
        """
        return f"{url.BASE}/{self._path if self._path else self.missing_path()}"

    async def save(
        self,
        file_name: str,
        path: typing.Union[pathlib.Path, str],
        /,
        mime_type: typing.Optional[typing.Union[MimeType, str]] = None,
    ) -> None:
        """Saves the image to a file.

        Parameters
        ----------
        file_name : `str`
            A name for the file to save the image to.
        path : `pathlib.Path | str`
            A path tp save the image to.

        Other Parameters
        ----------------
        mime_type : `MimeType | str`
            Optional MIME type of the image.

        Raises
        ------
        `FileNotFoundError`
            If the path provided does not exist.
        `RuntimeError`
            If the image could not be saved.
        `PermissionError`
            If the path provided is not writable or does not have write permissions.
        """
        if isinstance(path, pathlib.Path) and not path.exists():
            raise FileNotFoundError(f"File does not exist: {path!r}")

        if self.is_missing:
            return

        mimetype = mime_type or MimeType.PNG
        path = pathlib.Path(path)

        loop = helpers.get_or_make_loop()
        pool = concurrent.futures.ThreadPoolExecutor()

        try:
            with pool:
                await loop.run_in_executor(
                    pool, _write, path, file_name, mimetype, await self.read()
                )
                _LOGGER.info("Saved image to %s", file_name)

        except asyncio.CancelledError:
            pass

        except Exception as err:
            raise RuntimeError("Encountered an error while saving image.") from err

    async def read(self) -> bytes:
        """Read this image bytes.

        Returns
        -------
        `bytes`
            The bytes of this image.
        """
        client_session = aiohttp.ClientSession()

        try:
            await client_session.__aenter__()
            response = await client_session.get(self.create_url())

            if 300 >= response.status >= 200:
                reader = await response.read()

        except Exception as exc:
            raise RuntimeError(f"Failed to read image: {exc}") from None
        finally:
            await client_session.__aexit__(None, None, None)
        return reader

    async def iter(self) -> collections.AsyncGenerator[bytes, None]:
        """Iterates over the image bytes lazily.

        Example
        -------
        import aiobungie

        resource = aiobungie.Image("img/misc/missing_icon_d2.png")
        async for chunk in resource.iter():
            print(chunk)

        Returns
        -------
        `collections.AsyncGenerator[bytes, None]`
            An async generator of the image bytes.
        """

        async for chunk in self:
            yield chunk

    def __repr__(self) -> str:
        return f"Image(url={self.create_url()})"

    def __str__(self) -> str:
        return self.create_url()

    def __aiter__(self) -> Image:
        return self

    async def __anext__(self) -> bytes:
        return await self.read()

    def __await__(self) -> collections.Generator[None, None, bytes]:
        return self.__anext__().__await__()
