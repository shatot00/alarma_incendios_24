from pydantic import BaseModel

class Gas(BaseModel):
    """
    Represents a gas.
    """

    level: float

    class ConfigDict:
        from_attributes = True


class Fire(BaseModel):
    """
    Represents a fire.
    """

    level: float

    class ConfigDict:
        from_attributes = True

