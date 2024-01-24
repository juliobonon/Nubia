from aiohttp import ClientSession
from loguru import logger as log


class HTTP:
    _session = None

    @property
    async def session(self):
        if not self._session:
            async with ClientSession() as ss:
                self._session = ss

        return self._session

    async def get(self, url, headers):
        self.res = await self.session.get(url, headers)
        return self.res

    @property
    async def json(self, default: any = None):
        try:
            return await self.res.json()
        except Exception as e:
            log.error(e)
