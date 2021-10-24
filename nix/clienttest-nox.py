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
    if (cli_key := dotenv.get_key("./.env", "CLIENT_TOKEN")):
        os.environ['CLIENT_TOKEN'] = cli_key
except ImportError:
    pass

@nox.session(reuse_venv=True)
def client_test(session: nox.Session) -> None:
    if session.env.get("CLIENT_TOKEN") is None:
        session.error("CLIENT_TOKEN not found in env variables.")

    try:
        session.install('.')
        path = pathlib.Path("./tests/_raw/test_client.py")
        if path.exists() and path.is_file():
            shutil.copy(path, '.')
            session.run("python", 'test_client.py')
            session.log("======Speed ups======")

            if os.name != 'nt':
                # Avoid windows.
                try:
                    session.install("uvloop")
                    import uvloop
                except (ImportError, Exception) as exc:
                    session.log("Coulnd't install uvloop: %s", exc)
                    pass
                else:
                    uvloop.install()
            session.run("python", "-OO", 'test_client.py')
        os.remove("./test_client.py")
    except Exception:
        try:
            os.remove("./test_client.py")
        except FileNotFoundError:
            pass
