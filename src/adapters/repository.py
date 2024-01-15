import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import config
from src.models import Base
from src.models.warframe_item import WarframeItem


def create_db_session():
    engine = create_engine(config.get_postgres_uri())
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    return session()


database = create_db_session()


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku):
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    def get_by_batchref(self, batchref):
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_batchref(self, batchref):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, product, sku):
        return self.session.query(product).filter_by(sku=sku).first()
