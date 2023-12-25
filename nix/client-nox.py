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
import pathlib
import shutil
import os

try:
    import dotenv

    if cli_key := dotenv.get_key("./.env", "CLIENT_TOKEN"):
        os.environ["CLIENT_TOKEN"] = cli_key
except ModuleNotFoundError:
    pass


@nox.session(reuse_venv=True, name="client")
def client_test(session: nox.Session) -> None:
    session.install("python-dotenv")
    session.install("orjson")
    if session.env.get("CLIENT_TOKEN") is None:
        session.error("CLIENT_TOKEN not found in env variables.")

    session.install("-r", "requirements.txt")
    session.install(".", "--upgrade")
    path = pathlib.Path("./tests/aiobungie/test_client.py")
    try:
        if path.exists() and path.is_file():
            shutil.copy(path, ".")
            session.run("python", "test_client.py")
        os.remove("./test_client.py")
    finally:
        pathlib.Path("./test_client.py").unlink(missing_ok=True)
        session.run("pip", "uninstall", "aiobungie", "--yes", "-v", "--retries", "3")
