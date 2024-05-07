from sqlalchemy import Column, Integer, String, Float, DateTime

from .database import Base

class Gas(Base):
    """
    Represents an gas reading.

    Attributes:
        id (int): The unique identifier for the gas reading.
        time (datetime): The timestamp of the reading.
    """

    __tablename__ = "gas"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)
    x = Column(Float, primary_key=False, nullable=False, index=False)
    y = Column(Float, primary_key=False, nullable=False, index=False)
    z = Column(Float, primary_key=False, nullable=False, index=False)

class Fire(Base):
    """
    Represents a fire reading.

    Attributes:
        id (int): The unique identifier of the fire reading.
        time (datetime): The timestamp of the reading.
    """
    __tablename__ = "fire"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)

class Sprinkler(Base):
    """
    Represents a sprinkler.

    Attributes:
        id (int): The unique identifier of the sprinkler.
        time (datetime): The timestamp of the sprinkler.
    """

    __tablename__ = "sprinkler"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)

class Lcd(Base):
    """
    Represents a gyroscope measurement.

    Attributes:
        id (int): The unique identifier for the lcd.
        time (datetime): The timestamp of the measurement.
    """

    __tablename__ = "lcd"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)


class Buzzer(Base):
    """
    Represents a gyroscope measurement.

    Attributes:
        id (int): The unique identifier for the buzzer.
        time (datetime): The timestamp of the measurement.
    """

    __tablename__ = "buzzer"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)
