
from pydantic import BaseModel

class Trajectory(BaseModel):
    id: int
    description: str
    type: str
    number_of_products: int

