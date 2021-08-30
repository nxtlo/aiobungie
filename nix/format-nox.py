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

import nox

WORDS: list[str] = ["crate"]


@nox.session(reuse_venv=True)
def format(session: nox.Session) -> None:
    session.install("-r", "dev-requirements.txt")
    session.run("isort", ".")
    session.run("black", ".")


@nox.session(reuse_venv=True)
def check_black(session: nox.Session) -> None:
    session.install("black")
    session.run("black", ".", "--check")


@nox.session(reuse_venv=True)
def spell(session: nox.Session) -> None:
    session.install("codespell")
    session.run(
        "codespell",
        "aiobungie",
        "--write-changes",
        "-L",
        " ,".join(word for word in WORDS),
    )
