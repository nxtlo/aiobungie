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

import nox

FILES = [
    "aiobungie/__init__.py",
    "aiobungie/crates/__init__.py",
]


@nox.session(reuse_venv=True, name="stubgen")
def gen_stubs(session: nox.Session) -> None:
    session.install("-r", "requirements.txt", "-r", "dev-requirements.txt")
    session.run("stubgen", *FILES, "-o", ".", "--include-private", "--no-import")

    _paths = [p + "i" for p in FILES]
    session.run("python", "-m", "isort", *_paths)
    session.run("python", "-m", "ruff", "format", *_paths)


@nox.session(reuse_venv=True, name="type-check")
def type_check(session: nox.Session) -> None:
    session.install("-r", "requirements.txt", "-r", "dev-requirements.txt")
    session.run("python", "-m", "mypy", "aiobungie")
