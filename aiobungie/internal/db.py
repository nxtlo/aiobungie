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

"""A small sqlite3 database for the bungie manifest."""

import json
import logging
import sqlite3
import typing as t

log: t.Final[logging.Logger] = logging.getLogger(__name__)
log.setLevel("DEBUG")


class Database:
    __slots__: t.Sequence[str] = ("path", "_db", "_curs", "_version")

    def __init__(self, path: str) -> None:
        self.path = path
        self._db = sqlite3.connect(self.path, check_same_thread=True)
        self._curs = self._db.cursor()
        self._version: t.Optional[str] = None

    def commit(self) -> None:
        self._db.commit()
        log.debug("DB Commit.")

    def fetch(
        self, sql: str, params: tuple = None, get: t.Optional[t.Any] = None, /
    ) -> t.Any:
        if sql and isinstance(params, tuple):
            try:
                trans = self._curs.execute(sql, params)
                for row in trans:
                    if not get:
                        obj = json.loads(*row)
                    obj = json.loads(*row)[get]  # type: ignore
            except Exception:
                raise
        return obj

    def fetchrow(self, sql: str, params: tuple = None) -> t.Any:
        if row := self._curs.execute(sql, params).fetchall():  # type: ignore
            return [row[0]]

    def create_table(self, name, param: str, type: str) -> None:
        """Creates a table with one column, this is only used for the versions."""
        self._curs.execute(
            "CREATE TABLE IF NOT EXISTS {}({} {})".format(name, param, type)
        )

    def insert_version(self, version) -> None:
        """Insertes the manifest version."""
        self._curs.execute("INSERT INTO versions(version) VALUES(?)", (version,))
        self.commit()

    def execute(self, sql: str, params: tuple = None) -> None:
        self._curs.execute(sql, params)  # type: ignore

    def get_version(self) -> t.Union[str, None]:
        if (
            version := self._curs.execute("SELECT version FROM versions").fetchone()[0]
        ) is not None:
            return version
        return None

    @property
    def version(self) -> t.Optional[str]:
        return self.get_version()
