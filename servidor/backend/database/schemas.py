from pydantic import BaseModel

class Gas(BaseModel):
    """
    Represents a gas.
    """

    x: float
    y: float
    z: float

    class ConfigDict:
        from_attributes = True


class Fire(BaseModel):
    """
    Represents a fire.
    """

    x: float
    y: float
    z: float

    class ConfigDict:
        from_attributes = True


class Sprinkler(BaseModel):
    """
    Represents sprinkler.
    """

    latitude: float
    longitude: float

    class ConfigDict:
        from_attributes = True


class Lcd(BaseModel):
    """
    Represents a lcd.
    """

    x: float
    y: float
    z: float

    class ConfigDict:
        from_attributes = True



class Buzzer(BaseModel):
    """
    Represents a buzzer.

    Attributes:
        illuminance (int): The illuminance value measured by the sensor.
    """
    illuminance: int

    class ConfigDict:
        from_attributes = True

