# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2020 Nekokatt
# Copyright (c) 2021 davfsa
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

"""Basic lazy ratelimit systems for asyncio."""

from __future__ import annotations

__all__: tuple[str, ...] = ("ExponentialBackOff",)

import math
import random
import typing


@typing.final
class ExponentialBackOff:
    r"""Implementation of an asyncio-compatible exponential back-off algorithm with random jitter.
    .. math::
        t_{backoff} = b^{i} +  m \cdot \mathrm{rand}()
    Such that \(t_{backoff}\) is the backoff time, \(b\) is the base,
    \(i\) is the increment that increases by 1 for each invocation, and
    \(m\) is the jitter multiplier. \(\mathrm{rand}()\) returns a value in
    the range \([0,1]\).
    Parameters
    ----------
    base : builtins.float
        The base to use. Defaults to `2.0`.
    maximum : builtins.float
        The max value the backoff can be in a single iteration. Anything above
        this will be capped to this base value plus random jitter.
    jitter_multiplier : builtins.float
        The multiplier for the random jitter. Defaults to `1.0`.
        Set to `0` to disable jitter.
    initial_increment : builtins.int
        The initial increment to start at. Defaults to `0`.
    Raises
    ------
    ValueError
        If an `builtins.int` that's too big to be represented as a
        `builtins.float` or a non-finite value is passed in place of a field
        that's annotated as `builtins.float`.
    """

    __slots__ = (
        "base",
        "increment",
        "maximum",
        "jitter_multiplier",
    )

    base: typing.Final[float]
    """The base to use. Defaults to 2.0."""

    increment: int
    """The current increment."""

    maximum: float
    """This is the max value the backoff can be in a single iteration before an
    `asyncio.TimeoutError` is raised.
    """

    jitter_multiplier: typing.Final[float]
    """The multiplier for the random jitter.
    This defaults to `1.0`. Set to `0.0` to disable jitter.
    """

    def __init__(
        self,
        base: float = 2.0,
        maximum: float = 64.0,
        jitter_multiplier: float = 1.0,
        initial_increment: int = 0,
    ) -> None:
        # https://mypy.readthedocs.io/en/stable/duck_type_compatibility.html
        # Mypy makes the assumption that ints will always be compatible with floats, this isn't the case and could lead
        # to some edge cases that we'd be better off catching earlier on by ensuring these values are actually valid
        # (most notably floats have a system based maximum size whereas integers theoretically don't with implicit
        # conversion to a float raising an error if an integer that's too big to be a float is handled).
        try:
            self.base = float(base)
            self.maximum = float(maximum)
            self.jitter_multiplier = float(jitter_multiplier)
        except OverflowError:
            raise ValueError("int too large to be represented as a float") from None

        if not math.isfinite(self.base):
            raise ValueError("base must be a finite number") from None

        if not math.isfinite(self.maximum):
            raise ValueError("maximum must be a finite number") from None

        if not math.isfinite(self.jitter_multiplier):
            raise ValueError("jitter_multiplier must be a finite number") from None

        self.increment = initial_increment

    def __next__(self) -> float:
        """Get the next back off to sleep by."""
        try:
            value = self.base**self.increment

            if value >= self.maximum:
                value = self.maximum
            else:
                # This should only be incremented after we verify we haven't hit the maximum value.
                self.increment += 1
        except OverflowError:
            # If this happened then we can be sure that we've passed maximum.
            value = self.maximum

        return (
            value + random.random() * self.jitter_multiplier
        )  # nosec  # noqa S311 rng for cryptography

    def __iter__(self) -> ExponentialBackOff:
        """Return this object, as it is an iterator."""
        return self

    def reset(self) -> None:
        """Reset the exponential back-off."""
        self.increment = 0
