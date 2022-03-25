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

__all__: tuple[str, ...] = ("FlatIterator", "into_iter")

import collections.abc as collections
import itertools
import typing

Item = typing.TypeVar("Item")
"""A type hint for the item type of the iterator."""

if typing.TYPE_CHECKING:
    import _typeshed as typeshed

    OtherItem = typing.TypeVar("OtherItem")
    _B = typing.TypeVar("_B", bound=collections.Callable[..., typing.Any])


class FlatIterator(typing.Generic[Item]):
    """A Flat, In-Memory iterator for sequenced based data.

    This can either be used sync or asynchronously.

    Example
    -------
    ```py
    iterator = FlatIterator([1, 2, 3])

    # Limit the results to 2.
    async for item in iterator.take(2):
        print(item)
    # 1
    # 2

    # Filter the results.
    async for item in iterator.filter(lambda item: item > 1):
        print(item)
        print(iterator.count())
    # 2
    # 3
    # 3

    # Map the results.
    async for item in iterator.map(lambda item: item * 2):
        print(item)
    # 2
    # 4

    # This also works synchronously.
    iterator = FlatIterator(["Hello", "World", "!"])
    for item in iterator.discard(lambda item: "!" in item):
        print(item)
    # Hello
    # World

    # Indexing is also supported.

    print(iterator[0])
    # Hello
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
        """Collects all items in the iterator into a list and cast them into an object if provided.

        Example
        -------
        >>> iterator = FlatIterator([1, 2, 3])
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
        ...

    def collect(
        self, casting: typing.Optional[_B] = None
    ) -> typing.Union[list[Item], list[_B]]:
        """Collects all items in the iterator into a list.

        Example
        -------
        >>> iterator = FlatIterator([1, 2, 3])
        >>> iterator.collect()
        [1, 2, 3]

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
        >>> iterator = FlatIterator[str](["1", "2", "3"])
        item = iterator.next()
        assert item == "1"
        item = iterator.next()
        assert item == "2"

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
    ) -> FlatIterator[OtherItem]:
        """Maps each item in the iterator to its predicated value.

        Example
        -------
        >>> iterator = FlatIterator[str](["1", "2", "3"]).map(lambda value: int(value))
        <FlatIterator([1, 2, 3])>
        >>> async for item in iterator:
                assert isinstance(item, int)

        Parameters
        ----------
        predicate: `collections.Callable[[Item], Item]`
            The function to map each item in the iterator to its predicated value.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return FlatIterator(map(predicate, self._items))

    def take(self, n: int) -> FlatIterator[Item]:
        """Take the first number of items until the number of items are yielded or
        the end of the iterator is reached.

        Example
        -------
        >>> iterator = FlatIterator([GameMode.RAID, GameMode.STRIKE, GameMode.GAMBIT])
        >>> async for mode in iterator.take(2):
                assert mode in [GameMode.RAID, GameMode.STRIKE]
        <FlatIterator([GameMode.RAID, GameMode.STRIKE])>

        Parameters
        ----------
        n: `int`
            The number of items to take.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return FlatIterator(itertools.islice(self._items, n))

    def take_while(
        self, predicate: collections.Callable[[Item], bool]
    ) -> FlatIterator[Item]:
        """Yields items from the iterator while predicate returns `True`.

        Example
        -------
        ```py
        iterator = FlatIterator([MembershipType.STEAM, MembershipType.XBOX, MembershipType.STADIA])

        async for platform in (
            iterator
            .take_while(lambda platform: platform is not MembershipType.XBOX)
        ):
                print(platform)
        # <FlatIterator([MembershipType.STEAM])>
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
        return FlatIterator(itertools.takewhile(predicate, self._items))

    def drop_while(
        self, predicate: collections.Callable[[Item], bool]
    ) -> FlatIterator[Item]:
        """Yields items from the iterator while predicate returns `False`.

        Example
        -------
        ```py
        iterator = FlatIterator(
            [DestinyMembership(name="Fate"), DestinyMembership(name="Jim"), DestinyMembership(name="Bob")]
        )

        async for membership in (
            iterator
            .drop_while(lambda membership: membership.name is not "Jim")
        ):
                print(membership)
        # <FlatIterator([DestinyMembership(name="Bob")])>
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
        return FlatIterator(itertools.dropwhile(predicate, self._items))

    def filter(
        self, predicate: collections.Callable[[Item], bool]
    ) -> FlatIterator[Item]:
        """Filters the iterator to only yield items that match the predicate.

        Example
        -------
        ```py
        activities = FlatIterator(
            [Activity(mode=GameMode.RAID), Activity(mode=GameMode.DUNGEON), Activity(mode=GameMode.STRIKE)]
            # Assuming Raid is solo, Strike is flawless.
        )

        async for activity in (
            activities
            .filter(lambda activity: activity.is_solo or activity.is_flawless)
        ):
                print(member)
        # <FlatIterator([Activity(mode=GameMode.RAID), Activity(mode=GameMode.STRIKE)])>
        ```
        """
        return FlatIterator(filter(predicate, self._items))

    def skip(self, n: int) -> FlatIterator[Item]:
        """Skips the first number of items in the iterator.

        Example
        -------
        ```py
        iterator = FlatIterator([MembershipType.STEAM, MembershipType.XBOX, MembershipType.STADIA])

        async for platform in iterator.skip(1):
                print(platform)
        # Skip the first item in the iterator.
        # <FlatIterator([MembershipType.XBOX, MembershipType.STADIA])>
        """
        return FlatIterator(itertools.islice(self._items, n, None))

    def discard(
        self, predicate: collections.Callable[[Item], bool]
    ) -> FlatIterator[Item]:
        """Discards all elements in the iterator for which the predicate function returns true.

        Example
        -------
        >>> iterator = FlatIterator([MembershipType.STEAM, MembershipType.XBOX, MembershipType.STADIA])
        >>> async for _ in iterator.discard(lambda platform: platform is not MembershipType.STEAM):
                # Drops all memberships that are not steam.
                print(iterator)
        <FlatIterator([MembershipType.XBOX, MembershipType.STADIA])>

        Parameters
        ----------
        predicate: `collections.Callable[[Item], bool]`
            The function to test each item in the iterator.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return FlatIterator(filter(lambda x: not predicate(x), self._items))

    def zip(
        self, other: FlatIterator[OtherItem]
    ) -> FlatIterator[tuple[Item, OtherItem]]:
        """Zips the iterator with another iterable.

        Example
        -------
        >>> iterator = FlatIterator([1, 2, 3])
        >>> other = FlatIterator([4, 5, 6])
        >>> async for item, other_item in iterator.zip(other):
                assert item == other_item
        <FlatIterator([(1, 4), (2, 5), (3, 6)])>

        Parameters
        ----------
        other: `FlatIterator[OtherItem]`
            The iterable to zip with.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return FlatIterator(zip(self._items, other))

    def all(self, predicate: collections.Callable[[Item], bool]) -> bool:
        """`True` if all items in the iterator match the predicate.

        Example
        -------
        >>> iterator = FlatIterator([1, 2, 3])
        >>> while iterator.all(lambda item: isinstance(item, int)):
                print("Still all integers")
                continue
            # Still all integers

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
        >>> iterator = FlatIterator([1, 2, 3])
        >>> if iterator.any(lambda item: isinstance(item, int)):
                print("At least one item is an int.")
        # At least one item is an int.

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
    ) -> FlatIterator[Item]:
        """Sorts the iterator.

        Example
        -------
        >>> iterator = FlatIterator([3, 1, 6, 7])
        >>> async for item in iterator.sort(key=lambda item: item < 3):
                print(item)
        # 1
        # 3
        # 6
        # 7

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
        return FlatIterator(sorted(self._items, key=key, reverse=reverse))

    def first(self) -> Item:
        """Returns the first item in the iterator.

        Example
        -------
        >>> iterator = FlatIterator([3, 1, 6, 7])
        >>> iterator.first()
        3

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return self.take(1).next()

    def reversed(self) -> FlatIterator[Item]:
        """Returns a new iterator that yields the items in the iterator in reverse order.

        Example
        -------
        >>> iterator = FlatIterator([3, 1, 6, 7])
        >>> async for item in iterator.reversed():
                print(item)
        # 7
        # 6
        # 1
        # 3

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return FlatIterator(reversed(self.collect()))

    def count(self) -> int:
        count = 0
        for _ in self:
            count += 1

        return count

    def union(self, other: FlatIterator[Item]) -> FlatIterator[Item]:
        """Returns a new iterator that yields all items from both iterators.

        Example
        -------
        >>> iterator = FlatIterator([1, 2, 3])
        >>> other = FlatIterator([4, 5, 6])
        >>> async for item in iterator.union(other):
                print(item)
        # 1
        # 2
        # 3
        # 4
        # 5
        # 6

        Parameters
        ----------
        other: `FlatIterator[Item]`
            The iterable to union with.

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return FlatIterator(itertools.chain(self._items, other))

    def for_each(self, func: collections.Callable[[Item], typing.Any]) -> None:
        """Calls the function on each item in the iterator.

        Example
        -------
        >>> iterator = FlatIterator([1, 2, 3])
        >>> iterator.for_each(lambda item: print(item))
        # 1
        # 2
        # 3

        Parameters
        ----------
        func: `typeshed.Callable[[Item], None]`
            The function to call on each item in the iterator.
        """
        for item in self:
            func(item)

    def enumerate(self, *, start: int = 0) -> FlatIterator[tuple[int, Item]]:
        """Returns a new iterator that yields tuples of the index and item.

        Example
        -------
        >>> iterator = FlatIterator([1, 2, 3])
        >>> async for index, item in iterator.enumerate():
                print(index, item)

        # 0, 1
        # 1, 2
        # 2, 3

        Raises
        ------
        `StopIteration`
            If no elements are left in the iterator.
        """
        return FlatIterator(enumerate(self._items, start=start))

    def _ok(self) -> typing.NoReturn:
        raise StopIteration("No more items in the iterator.") from None

    def __getitem__(self, index: int) -> Item:
        try:
            return self.skip(index).first()
        except IndexError:
            self._ok()

    # This is a never.
    def __setitem__(self) -> typing.NoReturn:
        raise TypeError(
            f"{type(self).__name__} doesn't support item assignment."
        ) from None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({", ".join([str(item) for item in self])})>'

    def __len__(self) -> int:
        return self.count()

    # We support both sync and async iter.
    def __iter__(self) -> FlatIterator[Item]:
        return self

    def __aiter__(self) -> FlatIterator[Item]:
        return self

    def __next__(self) -> Item:
        try:
            item = next(self._items)
        except StopIteration:
            self._ok()

        return item

    async def __anext__(self) -> Item:
        try:
            item = next(self._items)
        except StopIteration as e:
            raise StopAsyncIteration from e

        return item


def into_iter(
    iterable: collections.Iterable[Item],
) -> FlatIterator[Item]:
    """Converts an iterable into an flat iterator.

    Example
    -------
    >>> sequence = [1,2,3]
    >>> async for item in aiobungie.into_iter(sequence).reversed():
            print(item)
    # 3
    # 2
    # 1

    Parameters
    ----------
    iterable: `typing.Iterable[Item]`
        The iterable to convert.

    Raises
    ------
    `StopIteration`
        If no elements are left in the iterator.
    """
    return FlatIterator(iterable)
