import os

import pytest
from PIL import Image

from src.image_process import DataProcessorProcess


class MockQueue:
    def __init__(self, image):
        self.image = image

    async def get(self):
        return self.image

    async def put(self, arg):
        pass


@pytest.mark.asyncio
async def test_image_process():
    """
    Tests the image processing.
    Grants that the processor is returning at least 5 items by image.
    """
    image = Image.open(os.path.join(os.getcwd() + "/preprocessed_image.jpg"))
    assert image
    processor: DataProcessorProcess = DataProcessorProcess(
        MockQueue(image), MockQueue(image)
    )

    await processor.run()
    assert processor.inventory.items
    assert len(processor.inventory.items) > 10
