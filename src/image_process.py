import asyncio
import io
from copy import copy

import easyocr
from loguru import logger as log
from PIL.Image import Image

from src.warframe_inventory import WarframeItem, WarframeUserInventory
from src.warframe_market import WarframeMarket


async def set_warframe_item_properties(
    item: dict,
    warframe_tradable_items: list,
    inventory: WarframeUserInventory,
    wf_market: WarframeMarket,
):
    item_info = warframe_tradable_items[item]
    wf_item = WarframeItem()
    wf_item.from_dict(item_info)

    if not inventory.item_in_list(wf_item):
        log.debug(f"{item} not in list")
        wf_item.set_platinum_price(await wf_market.get_price(item_info["url_name"]))
        wf_item.set_ducat_price(await wf_market.ducat_price(item_info["url_name"]))
        wf_item.set_item_image_url(
            await wf_market.item_image_url(item_info["url_name"])
        )
        inventory.add_to_batch(wf_item)


def item_in_list(
    warframe_market_items: dict,
    item_name: str,
):
    if not (clear_item := item_name.strip()):
        return False

    return any(
        clear_item in item["primary_name"] for item in warframe_market_items.values()
    )


class DataProcessorProcess:
    inventory = WarframeUserInventory()
    wf_market = WarframeMarket()
    ocr_reader = easyocr.Reader(["en"])

    def __init__(self, image_queue, data_queue):
        self.image_queue = image_queue
        self.data_queue = data_queue

    def image_to_bytes(self, image: Image) -> bytes:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        return img_byte_arr.getvalue()

    def read_ocr_items(self, image: bytes) -> list[tuple[list, str]]:
        """
        Items in the Warframe Inventory are organized in squares
        so we need to join close words to embrace multiple line items.
        """
        return self.ocr_reader.readtext(
            self.image_to_bytes(image),
            paragraph=True,
            y_ths=1.0,
        )

    async def process_image_data(self, image: Image):
        warframe_tradable_items = await self.wf_market.items
        ocr_items = self.read_ocr_items(image)

        filtered_items = list(
            filter(
                lambda item: item in warframe_tradable_items,
                map(lambda ocr_obj: ocr_obj[1], ocr_items),
            ),
        )

        # TODO: encapsulate into a method
        # TODO: implement semaphore to avoid rate limiting
        await asyncio.gather(
            *[
                set_warframe_item_properties(
                    wf_item,
                    warframe_tradable_items,
                    self.inventory,
                    self.wf_market,
                )
                for wf_item in filtered_items
            ]
        )

        return self.inventory

    async def run(self):
        """
        Principal loop method.
        Copies the items that are in the batch list and them clears it in order to avoid adding similar items.
        """
        log.info("Waiting for image data...")
        img_bytes: Image = await self.image_queue.get()

        log.info("Processing screenshot image")
        self.inventory = await self.process_image_data(img_bytes)

        if any(self.inventory.batch_items):
            log.info("There are some items to be added on database")
            items = copy(self.inventory.batch_items)
            self.inventory.batch_items.clear()
            await self.data_queue.put(items)
