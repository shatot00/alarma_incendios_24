from sqlalchemy import Column, Integer, String, Float, DateTime

from .database import Base

class Gas(Base):
    """
    Represents an gas reading.

    Attributes:
        id (int): The unique identifier for the gas reading.
        time (datetime): The timestamp of the reading.
        level (float): The level of the gas.
    """

    __tablename__ = "gas"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)
    level = Column(Float, primary_key=False, nullable=False, index=False)

class Fire(Base):
    """
    Represents a fire reading.

    Attributes:
        id (int): The unique identifier of the fire reading.
        time (datetime): The timestamp of the reading.
        level (float): The level of the fire.
    """
    __tablename__ = "fire"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)
    level = Column(Float, primary_key=False, nullable=False, index=False)
