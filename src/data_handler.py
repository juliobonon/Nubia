from asyncio import wait_for
from loguru import logger as log
from src.adapters.repository import database


class DataHandler:
    def __init__(self, data_queue):
        """
        Initializes the data handler which will be used
        to process data from the data queue and
        add it to the database.
        """
        self.database = database
        self.data_queue = data_queue

    def add_items_to_database(self, items):
        """
        Adds all items to the database
        """
        for item in items:
            if item.state == "DATABASE":
                log.info(f"Skipping {item.name}")
                continue

            item.state = "DATABASE"
            self.database.add(item)
            log.info(f"Adding {item.name} to database")

        self.database.commit()

    async def run(self):
        try:
            log.info("Waiting for image data...")
            wf_items = await wait_for(self.data_queue.get(), timeout=3)
            log.info(f"Processing {len(wf_items)} items...")
            self.add_items_to_database(wf_items)
        except TimeoutError:
            return
