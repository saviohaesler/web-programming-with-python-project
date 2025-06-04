from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class Apartment(SQLModel, table=True):
    __tablename__ = "apartments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    plz: int
    space: float
    rooms: float
    price: float
