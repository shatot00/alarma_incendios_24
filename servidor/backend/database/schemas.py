from pydantic import BaseModel

class Gas(BaseModel):
    """
    Represents a gas.
    """

    level: int

    class ConfigDict:
        from_attributes = True


class Fire(BaseModel):
    """
    Represents a fire.
    """

    level: int

    class ConfigDict:
        from_attributes = True

