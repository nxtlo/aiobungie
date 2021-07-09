import os
from aiobungie.ext import OAuth2, refresh
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

sch = AsyncIOScheduler()

load_dotenv("./.env")
TOKEN = str(os.environ.get('TOKEN'))
SECRET = str(os.environ.get('SECRET'))

class OAuth2Tests(OAuth2):
    def __init__(self, token: str, secret: str) -> None:
        self.token = token
        self.secret = secret
        super().__init__(token=token, secret=secret)

    async def auth_tests(self):
        print(await self.get_current_user())

client = OAuth2Tests(TOKEN, SECRET)

async def main() -> None:
    await client.auth_tests()
client.loop.run_until_complete(main())