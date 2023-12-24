from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import Mapped
from . import Base


class WarframeItem(Base):
    __tablename__ = "WarframeItem"

    item_id: Mapped[int] = Column(Integer, primary_key=True)
    text: Mapped[str] = Column(String(100))
    name: Mapped[str] = Column(String(100))
    left: Mapped[int] = Column(Integer)
    top: Mapped[int] = Column(Integer)
    confidence: Mapped[int] = Column(Integer)
    url_name: Mapped[str] = Column(String(100))
    primary_name: Mapped[str] = Column(String(100))
    platinum_price: Mapped[int] = Column(Integer)
    ducat_price: Mapped[int] = Column(Integer)
    item_image_url: Mapped[str] = Column(String(150))
    state: Mapped[str] = Column(String(100))

    def set_ducat_price(self, price):
        self.ducat_price = price

    def set_platinum_price(self, price):
        self.platinum_price = price

    def set_item_image_url(self, image_url):
        self.item_image_url = image_url

    @property
    def warframe_market_url(self):
        return f"warframe_market/items/{self.url_name}"

    def from_dict(self, dict):
        self.name = dict.get("item_name")
        self.left = dict.get("left")
        self.top = dict.get("top")
        self.confidence = dict.get("confidence")
        self.url_name = dict.get("url_name")

    def to_dict(self):
        item_dict = vars(self)
        return {
            name: value for name, value in item_dict.items() if not name.startswith("_")
        }
