from asyncio import wait_for
from asyncio.exceptions import TimeoutError

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
            try:
                log.info(f"Adding {item.name} to database")
                self.database.add(item)
                self.database.commit()
            except Exception as e:
                self.database.rollback()
                log.error(f"Error adding {item.name} to database {str(e)}")

    async def run(self):
        try:
            log.info("Waiting for image data...")
            wf_items = await wait_for(self.data_queue.get(), timeout=3)
            log.info(f"Processing {len(wf_items)} items...")
            self.add_items_to_database(wf_items)
        except TimeoutError:
            return
