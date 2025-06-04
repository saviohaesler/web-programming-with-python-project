from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, create_engine, SQLModel, select
import logging
import sys
import os

from db.model import Apartment
from db.repository_interface import RepositoryInterface

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


class PostgreSQLRepository(RepositoryInterface):

    def __init__(self, db_string=f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db:5432/apartments"):
        print("PostgreSQLRepository.__init__")
        print(f"db_string={db_string}")

        self.engine = create_engine(db_string)
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def add_apartments(self, apartments: list[Apartment]):
        for apartment in apartments:
            try:
                self.session.add(apartment)
            except IntegrityError as e:
                logging.error(e)
                logging.warning(
                    "Apartment was already recorded. apartment.id=%s", apartment.id
                )
                self.session.rollback()

        self.session.commit()

    def add_apartment(self, apartment: Apartment):
        try:
            self.session.add(apartment)
            self.session.commit()
        except IntegrityError as e:
            logging.error(e)
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
