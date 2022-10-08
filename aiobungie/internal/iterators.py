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
"""Module contains a Standard functional iterator implementation."""

from __future__ import annotations

__all__: tuple[str, ...] = ("Iterator", "into_iter")

import collections.abc as collections
import itertools
import typing

from . import helpers as _helpers

Item = typing.TypeVar("Item")
"""A type hint for the item type of the iterator."""

if typing.TYPE_CHECKING:
    import _typeshed as typeshed

    OtherItem = typing.TypeVar("OtherItem")
    _B = typing.TypeVar("_B", bound=collections.Callable[..., typing.Any])


class Iterator(typing.Generic[Item]):
    """A Flat, In-Memory iterator for sequenced based data.

    Example
    -------
    ```py
    iterator = Iterator([1, 2, 3])

    # Map the results.
    for item in iterator.map(lambda item: item * 2):
        print(item)
    # 2
    # 4

    # Indexing is also supported.
    print(iterator[0])
    # 1

    # Normal iteration.
    for item in iterator:
        print(item)
    # 1
    # 2
    # 3

    # Union two iterators.
    iterator2 = Iterator([4, 5, 6])
    final = iterator | iterator2
    # <Iterator([1, 2, 3, 4, 5, 6])>
    ```

    Parameters
    ----------
    items: `collections.Iterable[Item]`
        The items to iterate over.
    """

    __slots__ = ("_items",)

    def __init__(self, items: collections.Iterable[Item]) -> None:
        self._items = iter(items)

    @typing.overload
    def collect(self) -> list[Item]:
        ...

    @typing.overload
    def collect(self, casting: _B) -> list[_B]:
        ...

    def collect(
        self, casting: typing.Optional[_B] = None
    ) -> typing.Union[list[Item], list[_B]]:
        """Collects all items in the iterator into a list and cast them into an object if provided.

        Example
        -------
        >>> iterator = Iterator([1, 2, 3])
        >>> iterator.collect(casting=str)
        ["1", "2", "3"]

        Parameters
        ----------
        casting: `T | None`
            The type to cast the items to. If `None` is provided, the items will be returned as is.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        if casting is not None:
            return typing.cast(list[_B], list(map(casting, self._items)))

        return list(self._items)

    def next(self) -> Item:
        """Returns the next item in the iterator.

        Example
        -------
        ```py
        iterator = Iterator(["1", "2", "3"])
        item = iterator.next()
        assert item == "1"
        item = iterator.next()
        assert item == "2"
        ```

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        try:
            return self.__next__()
        except StopIteration:
            self._ok()

    def map(
        self, predicate: collections.Callable[[Item], OtherItem]
    ) -> Iterator[OtherItem]:
        """Maps each item in the iterator to its predicated value.

        Example
        -------
        ```py
        iterator = Iterator(["1", "2", "3"]).map(lambda value: int(value))
        print(iterator)
        # <Iterator([1, 2, 3])>
        ```

        Parameters
        ----------
        predicate: `collections.Callable[[Item], OtherItem]`
            The function to map each item in the iterator to its predicated value.

        Returns
        -------
        `Iterator[OtherItem]`
            The mapped iterator.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return Iterator(map(predicate, self._items))

    def take(self, n: int) -> Iterator[Item]:
        """Take the first number of items until the number of items are yielded or
        the end of the iterator is reached.

        Example
        -------
        ```py
        iterator = Iterator([GameMode.RAID, GameMode.STRIKE, GameMode.GAMBIT])
        print(iterator.take(2))
        # <Iterator([GameMode.RAID, GameMode.STRIKE])>
        ```

        Parameters
        ----------
        n: `int`
            The number of items to take.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return Iterator(itertools.islice(self._items, n))

    def take_while(
        self, predicate: collections.Callable[[Item], bool]
    ) -> Iterator[Item]:
        """Yields items from the iterator while predicate returns `True`.

        Example
        -------
        ```py
        iterator = Iterator([STEAM, XBOX, STADIA])
        print(iterator.take_while(lambda platform: platform is not XBOX))
        # <Iterator([STEAM])>
        ```

        Parameters
        ----------
        predicate: `collections.Callable[[Item], bool]`
            The function to predicate each item in the iterator.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return Iterator(itertools.takewhile(predicate, self._items))

    def drop_while(
        self, predicate: collections.Callable[[Item], bool]
    ) -> Iterator[Item]:
        """Yields items from the iterator while predicate returns `False`.

        Example
        -------
        ```py
        iterator = Iterator([DestinyMembership(name="Jim"), DestinyMembership(name="Bob")])
        print(iterator.drop_while(lambda membership: membership.name is not "Jim"))
        # <Iterator([DestinyMembership(name="Bob")])>
        ```

        Parameters
        ----------
        predicate: `collections.Callable[[Item], bool]`
            The function to predicate each item in the iterator.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return Iterator(itertools.dropwhile(predicate, self._items))

    def filter(self, predicate: collections.Callable[[Item], bool]) -> Iterator[Item]:
        """Filters the iterator to only yield items that match the predicate.

        Example
        -------
        ```py
        names = Iterator(["Jim", "Bob", "Mike", "Jess"])
        print(names.filter(lambda n: n != "Jim"))
        # <Iterator(["Bob", "Mike", "Jess"])>
        ```
        """
        return Iterator(filter(predicate, self._items))

    def skip(self, n: int) -> Iterator[Item]:
        """Skips the first number of items in the iterator.

        Example
        -------
        ```py
        iterator = Iterator([STEAM, XBOX, STADIA])
        print(iterator.skip(1))
        # <Iterator([XBOX, STADIA])>
        ```
        """
        return Iterator(itertools.islice(self._items, n, None))

    def zip(self, other: Iterator[OtherItem]) -> Iterator[tuple[Item, OtherItem]]:
        """Zips the iterator with another iterable.

        Example
        -------
        ```py
        iterator = Iterator([1, 3, 5])
        other = Iterator([2, 4, 6])
        for item, other_item in iterator.zip(other):
            print(item, other_item)
        # <Iterator([(1, 2), (3, 4), (5, 6)])>
        ```

        Parameters
        ----------
        other: `Iterator[OtherItem]`
            The iterable to zip with.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return Iterator(zip(self._items, other))

    def all(self, predicate: collections.Callable[[Item], bool]) -> bool:
        """`True` if all items in the iterator match the predicate.

        Example
        -------
        ```py
        iterator = Iterator([1, 2, 3])
        while iterator.all(lambda item: isinstance(item, int)):
            print("Still all integers")
            continue
        # Still all integers
        ```

        Parameters
        ----------
        predicate: `collections.Callable[[Item], bool]`
            The function to test each item in the iterator.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return all(predicate(item) for item in self)

    def any(self, predicate: collections.Callable[[Item], bool]) -> bool:
        """`True` if any items in the iterator match the predicate.

        Example
        -------
        ```py
        iterator = Iterator([1, 2, 3])
        if iterator.any(lambda item: isinstance(item, int)):
            print("At least one item is an int.")
        # At least one item is an int.
        ```

        Parameters
        ----------
        predicate: `collections.Callable[[Item], bool]`
            The function to test each item in the iterator.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return any(predicate(item) for item in self)

    def sort(
        self,
        *,
        key: collections.Callable[[Item], typeshed.SupportsRichComparison],
        reverse: bool = False,
    ) -> Iterator[Item]:
        """Sorts the iterator.

        Example
        -------
        ```py
        iterator = Iterator([3, 1, 6, 7])
        print(iterator.sort(key=lambda item: item))
        # <Iterator([1, 3, 6, 7])>
        ```

        Parameters
        ----------
        key: `collections.Callable[[Item], Any]`
            The function to sort by.
        reverse: `bool`
            Whether to reverse the sort.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return Iterator(sorted(self._items, key=key, reverse=reverse))

    def first(self) -> Item:
        """Returns the first item in the iterator.

        Example
        -------
        ```py
        iterator = Iterator([3, 1, 6, 7])
        print(iterator.first())
        3
        ```

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return self.take(1).next()

    def reversed(self) -> Iterator[Item]:
        """Returns a new iterator that yields the items in the iterator in reverse order.

        Example
        -------
        ```py
        iterator = Iterator([3, 1, 6, 7])
        print(iterator.reversed())
        # <Iterator([7, 6, 1, 3])>
        ```

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return Iterator(reversed(self.collect()))

    def count(self) -> int:
        """Returns the number of items in the iterator.

        Example
        -------
        ```py
        iterator = Iterator([3, 1, 6, 7])
        print(iterator.count())
        4
        ```
        """
        count = 0
        for _ in self:
            count += 1

        return count

    def union(self, other: Iterator[Item]) -> Iterator[Item]:
        """Returns a new iterator that yields all items from both iterators.

        Example
        -------
        ```py
        iterator = Iterator([1, 2, 3])
        other = Iterator([4, 5, 6])
        print(iterator.union(other))
        # <Iterator([1, 2, 3, 4, 5, 6])>
        ```

        Parameters
        ----------
        other: `Iterator[Item]`
            The iterable to union with.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return Iterator(itertools.chain(self._items, other))

    def for_each(self, func: collections.Callable[[Item], typing.Any]) -> None:
        """Calls the function on each item in the iterator.

        Example
        -------
        ```py
        iterator = Iterator([1, 2, 3])
        iterator.for_each(lambda item: print(item))
        # 1
        # 2
        # 3
        ```

        Parameters
        ----------
        func: `typeshed.Callable[[Item], None]`
            The function to call on each item in the iterator.
        """
        for item in self:
            func(item)

    async def async_for_each(
        self,
        func: collections.Callable[[Item], collections.Coroutine[None, None, None]],
    ) -> None:
        """Calls the async function on each item in the iterator concurrently.

        Example
        -------
        ```py
        async def signup(username: str) -> None:
            async with aiohttp.request('POST', '...') as r:
                # Actual logic.
                ...

        async def main():
            users = aiobungie.into_iter(["user_danny", "user_jojo"])
            await users.async_for_each(lambda username: signup(username))
        ```

        Parameters
        ----------
        func: `collections.Callable[[Item], collections.Coroutine[None, None, None]]`
            The async function to call on each item in the iterator.
        """
        await _helpers.awaits(*(func(item) for item in self))

    def enumerate(self, *, start: int = 0) -> Iterator[tuple[int, Item]]:
        """Returns a new iterator that yields tuples of the index and item.

        Example
        -------
        ```py
        iterator = Iterator([1, 2, 3])
        for index, item in iterator.enumerate():
            print(index, item)
        # 0 1
        # 1 2
        # 2 3
        ```

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return Iterator(enumerate(self._items, start=start))

    def _ok(self) -> typing.NoReturn:
        raise StopIteration("No more items in the iterator.") from None

    def __getitem__(self, index: int) -> Item:
        try:
            return self.skip(index).first()
        except IndexError:
            self._ok()

    def __or__(self, other: Iterator[Item]) -> Iterator[Item]:
        return self.union(other)

    # This is a never.
    def __setitem__(self) -> typing.NoReturn:
        raise TypeError(
            f"{type(self).__name__} doesn't support item assignment."
        ) from None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({", ".join([str(item) for item in self])})>'

    def __len__(self) -> int:
        return self.count()

    def __iter__(self) -> Iterator[Item]:
        return self

    def __next__(self) -> Item:
        try:
            item = next(self._items)
        except StopIteration:
            self._ok()

        return item


def into_iter(
    iterable: collections.Iterable[Item],
) -> Iterator[Item]:
    """Transform an iterable into an flat iterator.

    Example
    -------
    ```py
    sequence = [1,2,3]
    for item in aiobungie.into_iter(sequence).reversed():
        print(item)
    # 3
    # 2
    # 1
    ```

    Parameters
    ----------
    iterable: `typing.Iterable[Item]`
        The iterable to convert.

    Raises
    ------
    `StopIteration`
        If no elements are left in the iterator.
    """
    return Iterator(iterable)
