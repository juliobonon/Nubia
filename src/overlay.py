from PIL import ImageGrab, Image
from loguru import logger as log
import time
import asyncio


class Overlay:
    """
    Overlay class for capturing screenshots and saving them to memory
    for further processing.
    """

    def __init__(
        self,
        capture_interval: int | None,
        image_queue: asyncio.Queue,
    ):
        self.capture_interval = (
            capture_interval  # Time interval between captures (in seconds)
        )
        self.image_queue = image_queue

    async def run(self):
        screenshot: Image.Image = ImageGrab.grab()
        await self.image_queue.put(screenshot)
        log.info("Captured screenshot.")
        time.sleep(self.capture_interval)


# Example usage
if __name__ == "__main__":
    capture_interval = 5  # Capture interval in seconds (adjust as needed)
    processor = Overlay(capture_interval, asyncio.Queue())
    processor.run()
