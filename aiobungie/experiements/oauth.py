'''
MIT License

Copyright (c) 2020 - Present nxtlo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import httpx
import uuid
import sqlite3
import asyncio
import time
import inspect
import logging
from ..utils import Crypt, Time
from datetime import datetime
from typing import Callable, Any, Sequence, TYPE_CHECKING, Optional
from os.path import isfile
from requests_oauthlib import OAuth2Session
from functools import wraps

CLIENT_ID: int = 33953
TOKEN_EP: str = 'https://www.bungie.net/platform/app/oauth/token/'
AUTH_EP: str = 'https://www.bungie.net/en/OAuth/Authorize/'
REDIRECT: str = 'https://www.bungie.net/Platform'

log = logging.getLogger(__name__)
_db = sqlite3.connect('./db.sqlite')
_cur = _db.cursor()

__all__: Sequence[str] = (
	'OAuth2', 'refresh'
)

def on_ready():
	'''
	a decorator that literally just creates the database tables.
	'''
	def fake(inject: object):
		@wraps(inject)
		def decorator(*args, **kwargs):
			if isfile('./db.sqlite'):
				_cur.execute('''
				CREATE TABLE IF NOT EXISTS tokens(
					token TEXT PRIMARY KEY NOT NULL,
					refresh_token TEXT NOT NULL,
					token_author INT NOT NULL,
					inserted_at TIMESTAMP WITH TIME ZONE NOT NULL,
					updated_at TIMESTAMP WITH TIME ZONE NOT NULL
					);
				''')
			return inject(*args, **kwargs)
		return decorator
	return fake
class OAuth2:
	"""
	an exmepremental bungie oauth2

	Attributes
	-----------
	token: :class:`str`:
		Your application's token or API Key

	secret: :class:`str`:
		Your application's client secret.

	session: Optional[:class:`httpx.AsyncClient`]
		the http client session
	"""
	__slots__: Sequence[str] = (
		'_session', '_token', '_secret', '_loop'
	)

	if TYPE_CHECKING:
		_session: httpx.AsyncClient()
		_token: str
		_secret: str
		_loop: asyncio.get_event_loop()

	def __init__(self, token: str, secret: str, loop = None, session = None) -> None:
		self._token = token
		self._loop = asyncio.get_event_loop() if not loop else loop
		self._secret = secret
		if self._token is None:
			raise ValueError("Token have to be passed.")

		if self._secret is None:
			raise ValueError("Client Secret has to be passed.")

		self._session = session


	def __repr__(self) -> str:
		return f'<{self.__class__.__name__} Session: {self._session.__repr__} Status: {self._session._state}>'


	async def __aenter__(self) -> None:
		return await self._session.__aenter__()


	async def __aexit__(self, type = None, value = None, tb = None) -> None:
		return await self._session.__aexit__(type, value, tb)


	async def new_session(self) -> httpx.AsyncClient:
		self._session = httpx.AsyncClient()

	
	async def teardown(self) -> None:
		if not self._session.is_closed:
			log.warn("Shutting down now!...")
			await self._session.aclose()
		self._session = None


	async def run(self, path, aceess) -> Optional[httpx.Request]:
		if not self._session:
			await self.new_session()

		async with self._session as client:
			resp = await client.get(f'{REDIRECT}/{path}', headers={
				'X-API-KEY': self._token,
				'Authorization': f'Bearer {aceess}'
			})
			try:
				return resp.json().get('Response')
			except Exception: 
				return resp.text

	@on_ready()
	async def do_auth(self) -> None:
		req = OAuth2Session(
			client_id=CLIENT_ID, 
			redirect_uri='https://www.bungie.net/', 
			auto_refresh_url='https://www.bungie.net/Platform/App/OAuth/token/'
			)
		url, session = req.authorization_url(
			AUTH_EP, state=uuid.uuid4()
		)
		exists = _cur.execute("SELECT token FROM tokens")
		found = None
		try:
			found = exists.fetchall()[0][0]
		except IndexError: # token is out of index.
			print(url)
			wait = input("Please click the url and Enter the code: ")
			ok = req.fetch_token(TOKEN_EP, code=wait, client_secret=self._secret)
			access_token = ok.get('access_token')
			refresh_token = ok.get('refresh_token')
			_cur.execute("INSERT INTO tokens(token, refresh_token, inserted_at) VALUES(?, ?, ?)", (access_token, refresh_token, Time.clean_date(datetime.utcnow())))
			_db.commit()
			log.info("Inserted token to the database.")
		return found

	def get_token(self) -> str:
		return _cur.execute("SELECT token FROM tokens").fetchall()[0][0]

	async def get_current_user(self) -> Optional[httpx.Request]:
		return await self.run('User/GetBungieNetUser/', self.get_token())

def refresh(*, every: float = 0, cls = None) -> Callable[[Any], asyncio.AbstractEventLoop]:
	'''
	a decorator to refresh the token every ??? seconds.

	Paramaters
	----------
	every: :class:`float`:
		The amount of seconds to refresh after. Default is 60
	
	cls: :cls:`cls`::
		This should your OAuth2 class.
	
	Raises
	-------
	TypeError:
		The function was not a coroutine.
	'''
	if cls is None:
		cls = OAuth2
	def inner(inject: object):
		@wraps(inject)
		async def decorator(*args, **kwargs) -> None:
			ref_token = _cur.execute("SELECT refresh_token FROM tokens").fetchall()[0][0]
			async with httpx.AsyncClient() as client:
				request = await client.post(f'https://www.bungie.net/Platform/App/OAuth/token/', 
					data={
					'grant_type': 'refresh_token',
					'refresh_token': ref_token,
					'client_id': CLIENT_ID,
					'client_secret': cls._secret
				})
				req = request.json()
				new_token = req.get('access_token')
				new_ref = req.get('refresh_token')
				_cur.execute("UPDATE tokens SET (token, refresh_token, updated_at) = (?, ?, ?)", (new_token, new_ref, Time.clean_date(datetime.utcnow())))
				log.info(f"Tokens refreshed, sleeping for {every}.")
				if inspect.iscoroutinefunction(inject):
					await asyncio.sleep(every)
				else:
					raise TypeError(f"Expected coroutine function, not {type(inject).__name__!r}")
			coro = await inject(*args, **kwargs)
			await cls._loop.create_task(decorator())
			return coro
		return decorator
	return inner