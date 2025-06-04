from abc import ABC, abstractmethod

from db.model import Apartment


class RepositoryInterface(ABC):
    @abstractmethod
    def add_apartments(self, apartments: list[Apartment]):
        pass

    @abstractmethod
    def add_apartment(self, apartment: Apartment):
        pass

    @abstractmethod
    def get_apartments(self) -> list[Apartment]:
        pass
