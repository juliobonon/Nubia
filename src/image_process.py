import asyncio
from copy import copy

import pytesseract
from loguru import logger as log

from src.settings import TESSERACT_CMD
from src.warframe_inventory import WarframeItem, WarframeUserInventory
from src.warframe_market import WarframeMarket

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


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


def join_words_dictionaries(word_boxes: dict) -> list:
    return [
        {
            "text": word_boxes["text"][indx],
            "left": word_boxes["left"][indx],
            "top": word_boxes["top"][indx],
            "width": word_boxes["width"][indx],
            "height": word_boxes["height"][indx],
            "confidence": word_boxes["conf"][indx],
        }
        for indx in range(len(word_boxes["text"]))
    ]


def retrieve_close_words(
    word: dict,
    word_list: list,
    horizontal_threshold: int = 100,
    vertical_threshold: int = 60,
):
    return [
        word_in_list
        for word_in_list in word_list
        if abs(word["top"] - word_in_list["top"]) <= vertical_threshold
        and abs(word["left"] - word_in_list["left"]) <= horizontal_threshold
    ]


def build_item_full_name(
    word: dict,
    words_list: list,
    top_threshold: int = 10,
):
    # sort by top (items are organized in squares)

    final_desc = []
    for word_a in words_list:
        if (
            abs(word_a["top"] - word["top"]) <= top_threshold
            and word_a["text"] not in final_desc
        ):
            final_desc.append(word_a["text"])

    for word_a in words_list:
        if (
            abs(word_a["top"] - word["top"]) >= top_threshold
            and word_a["text"] not in final_desc
        ):
            final_desc.append(word_a["text"])

    return " ".join(item for item in final_desc)


def pre_process_image(img):
    grayscale_img = img.convert("L")

    return grayscale_img


class DataProcessorProcess:
    inventory = WarframeUserInventory()
    wf_market = WarframeMarket()

    def __init__(self, image_queue, data_queue):
        self.image_queue = image_queue
        self.data_queue = data_queue

    async def process_image_data(self, word_boxes: dict):
        word_groups = []  # List to store groups of words
        words_info = join_words_dictionaries(word_boxes)

        # sort words by left property
        sorted_words_info = sorted(words_info, key=lambda x: x["left"], reverse=False)

        warframe_market = WarframeMarket()
        warframe_tradable_items = await warframe_market.items

        for word in sorted_words_info:
            if not item_in_list(warframe_tradable_items, word["text"]):
                continue

            close_words = retrieve_close_words(word, sorted_words_info)

            # sort by left
            all_words = sorted(
                [word] + list(close_words), key=lambda x: x["left"], reverse=False
            )

            word_groups.append(build_item_full_name(word, all_words))

        filtered_items = list(
            filter(lambda item: item in warframe_tradable_items, word_groups)
        )

        # TODO: encapsulate into a method
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
        img_bytes = await self.image_queue.get()

        screenshot = pre_process_image(img_bytes)
        log.info("Processing screenshot image")

        ocr_dict_data = pytesseract.image_to_data(
            screenshot, lang="eng", output_type=pytesseract.Output.DICT
        )
        wf_inventory = await self.process_image_data(ocr_dict_data)
        log.debug(wf_inventory)

        if any(wf_inventory.batch_items):
            log.info("There are some items to be added on database")
            items = copy(wf_inventory.batch_items)
            wf_inventory.batch_items.clear()
            await self.data_queue.put(items)
