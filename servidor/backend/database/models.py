from sqlalchemy import Column, Integer, String, Float, DateTime

from .database import Base

class Accelerometer(Base):
    """
    Represents an accelerometer reading.

    Attributes:
        id (int): The unique identifier for the accelerometer reading.
        time (datetime): The timestamp of the accelerometer reading.
        x (float): The x-axis value of the accelerometer reading.
        y (float): The y-axis value of the accelerometer reading.
        z (float): The z-axis value of the accelerometer reading.
    """

    __tablename__ = "accelerometer"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)
    x = Column(Float, primary_key=False, nullable=False, index=False)
    y = Column(Float, primary_key=False, nullable=False, index=False)
    z = Column(Float, primary_key=False, nullable=False, index=False)

class Magnetometer(Base):
    """
    Represents a magnetometer reading.

    Attributes:
        id (int): The unique identifier of the magnetometer reading.
        time (datetime): The timestamp of the reading.
        x (float): The x-axis value of the magnetic field.
        y (float): The y-axis value of the magnetic field.
        z (float): The z-axis value of the magnetic field.
    """
    __tablename__ = "magnetometer"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)
    x = Column(Float, primary_key=False, nullable=False, index=False)
    y = Column(Float, primary_key=False, nullable=False, index=False)
    z = Column(Float, primary_key=False, nullable=False, index=False)

class GPS(Base):
    """
    Represents a GPS location.

    Attributes:
        id (int): The unique identifier of the GPS location.
        time (datetime): The timestamp of the GPS location.
        latitude (float): The latitude coordinate of the GPS location.
        longitude (float): The longitude coordinate of the GPS location.
    """

    __tablename__ = "gps"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    latitude = Column(Float, primary_key=False, nullable=False, index=False)
    longitude = Column(Float, primary_key=False, nullable=False, index=False)

class Gyroscope(Base):
    """
    Represents a gyroscope measurement.

    Attributes:
        id (int): The unique identifier for the gyroscope measurement.
        time (datetime): The timestamp of the measurement.
        x (float): The x-axis value of the gyroscope measurement.
        y (float): The y-axis value of the gyroscope measurement.
        z (float): The z-axis value of the gyroscope measurement.
    """

    __tablename__ = "gyroscope"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)
    x = Column(Float, primary_key=False, nullable=False, index=False)
    y = Column(Float, primary_key=False, nullable=False, index=False)
    z = Column(Float, primary_key=False, nullable=False, index=False)


class LightSensor(Base):

    __tablename__ = "lightsensor"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    time = Column(DateTime, primary_key=False, nullable=False, index=False)
    illuminance = Column(Integer, primary_key=False, nullable=False, index=False)
