import asyncio
from src.overlay import Overlay
from src.image_process import DataProcessorProcess
from src.data_handler import DataHandler
from typing import List, Callable, Awaitable


class Cephalon:
    tasks: List[Callable[[], Awaitable]] = []

    def __init__(self):
        self.image_queue = asyncio.Queue()
        self.data_queue = asyncio.Queue()

        self.tasks = [
            Overlay(capture_interval=5, image_queue=self.image_queue).run,
            DataProcessorProcess(
                image_queue=self.image_queue, data_queue=self.data_queue
            ).run,
            DataHandler(data_queue=self.data_queue).run,
            *self.tasks,
        ]

    async def run(self):
        """
        Runs the main loop that handles all the tasks.
        """
        while True:
            await asyncio.gather(*[task() for task in self.tasks])


if __name__ == "__main__":
    cel = Cephalon()
    asyncio.run(cel.run())
