from loguru import logger as log
from src.models.warframe_item import WarframeItem
from src.adapters.repository import database


class WarframeUserInventory:
    _items = list()
    _batch_items = list()

    def __init__(self):
        self.database = database

    def get_items_from_database(self):
        """
        Returns a list of all items from the database
        """
        return self.database.query(WarframeItem).all()

    @property
    def items(self):
        self._items = self.get_items_from_database()
        return self._items

    @property
    def batch_items(self):
        return self._batch_items

    def inventory_plat_price(self) -> float:
        return sum(item.platinum_price for item in self.items)

    def inventory_ducat_price(self) -> float:
        return sum(item.ducat_price for item in self.items)

    def add_to_batch(self, item: WarframeItem):
        self._batch_items.append(item)

    def add_item(self, item: WarframeItem):
        self._items.append(item)

    def remove_item(self, item: WarframeItem):
        self._items.remove(item)

    def item_in_list(self, item: WarframeItem):
        return any(item.name == list_item.name for list_item in self.items)
