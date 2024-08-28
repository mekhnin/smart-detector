from pydantic import BaseModel


class ArrayModel(BaseModel):
    array: str
