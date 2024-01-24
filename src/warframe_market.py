from aiohttp import ClientSession
from loguru import logger as log

WARFRAME_MARKET_ITEMS_URL = "https://api.warframe.market/v1/items"
WARFRAME_MARKET_ITEM_URL = "https://api.warframe.market/v1/items/{}"
WARFRAME_MARKET_ORDERS_URL = "https://api.warframe.market/v1/items/{}/orders"
WARFRAME_MARKET_ITEM_IMAGE_URL = "https://warframe.market/static/assets/{}"
ItemAPIJson = dict[str, str | int]


class WarframeMarket:
    _items = {}
    _items_api_info = {}

    async def get_tradable_warframe_items(self):
        async with ClientSession() as ss:
            res = await ss.get(
                url=WARFRAME_MARKET_ITEMS_URL, headers={"accept": "application/json"}
            )
            res_json = await res.json()
            return res_json["payload"]["items"]

    @property
    async def items(self):
        if not self._items:
            wf_items = await self.get_tradable_warframe_items()
            self._items = {
                item["item_name"]: {
                    **item,
                    "primary_name": item["item_name"].split()[0],
                }
                for item in wf_items
            }

        return self._items

    @property
    async def item_names(self):
        return [item["item_name"] for item in await self.items]

    @property
    async def item_primary_names(self):
        return set(item["item_name"].split()[0] for item in await self.items)

    async def get_item_api_info(self, item_name: str) -> ItemAPIJson:
        log.info(f"Getting ducat value for item {item_name}")

        async with ClientSession() as ss:
            try:
                res = await ss.get(
                    url=WARFRAME_MARKET_ITEM_URL.format(item_name),
                    headers={"accept": "application/json"},
                )
                if res.status == 429:
                    return {}

                res_json = await res.json()
                return res_json["payload"]["item"]["items_in_set"][0]
            except Exception as e:
                log.error(e)
                return {}

    async def items_api_info(self, item_name: str) -> ItemAPIJson:
        if not self._items_api_info.get(item_name):
            self._items_api_info[item_name] = await self.get_item_api_info(item_name)

        return self._items_api_info[item_name]

    async def ducat_price(self, item_name: str) -> int:
        return (await self.items_api_info(item_name)).get("ducats")

    async def item_image_url(self, item_name: str) -> str:
        return WARFRAME_MARKET_ITEM_IMAGE_URL.format(
            (await self.items_api_info(item_name)).get("thumb")
        )

    @staticmethod
    async def get_price(item_name) -> int:
        log.info(f"Getting price for item {item_name}")

        async with ClientSession() as ss:
            try:
                res = await ss.get(
                    url=WARFRAME_MARKET_ORDERS_URL.format(item_name),
                    headers={"accept": "application/json"},
                )
                if res.status == 429:
                    # TODO: fix rate limit by applying Semaphore
                    return 0

                res_json = await res.json()
                return res_json["payload"]["orders"][0]["platinum"]
            except Exception as e:
                log.error(e)
                return 0
