from pydantic import BaseModel

class Accelerometer(BaseModel):
    """
    Represents an accelerometer reading with x, y, and z coordinates.
    """

    x: float
    y: float
    z: float

    class ConfigDict:
        from_attributes = True


class Magnetometer(BaseModel):
    """
    Represents a magnetometer reading with x, y, and z coordinates.
    """

    x: float
    y: float
    z: float

    class ConfigDict:
        from_attributes = True


class GPS(BaseModel):
    """
    Represents GPS coordinates with latitude and longitude.
    """

    latitude: float
    longitude: float

    class ConfigDict:
        from_attributes = True


class Gyroscope(BaseModel):
    """
    Represents a gyroscope with x, y, and z coordinates.
    """

    x: float
    y: float
    z: float

    class ConfigDict:
        from_attributes = True



class LightSensor(BaseModel):
    """
    Represents a light sensor.

    Attributes:
        illuminance (int): The illuminance value measured by the sensor.
    """
    illuminance: int

    class ConfigDict:
        from_attributes = True

