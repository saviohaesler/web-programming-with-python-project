from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, create_engine, SQLModel, select
import logging
import sys

from db.model import Apartment
from db.repository_interface import RepositoryInterface

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


class SQLiteRepository(RepositoryInterface):
    def __init__(self, db_string="sqlite:///apartments.db"):
        self.engine = create_engine(db_string)
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def add_apartments(self, apartments: list[Apartment]):
        for apartment in apartments:
            try:
                self.session.add(apartment)
            except IntegrityError:
                logging.warning("Apartment already recorded: Id={}", apartment.id)
                self.session.rollback()

        self.session.commit()

    def add_apartment(self, apartment: Apartment):
        try:
            self.session.add(apartment)
            self.session.commit()
        except IntegrityError:
            logging.warning(
                "Apartment was already recorded. apartment.id=%s", apartment.id
            )
            self.session.rollback()

    def get_apartments(self) -> list[dict]:
        statement = select(Apartment)

        logging.info("Fetching apartments...")
        apartments = self.session.exec(statement).all()
        logging.info("Fetched apartments. count=%s", len(apartments))

        return [apartment.model_dump() for apartment in apartments]
