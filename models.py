from pydantic import BaseModel


class product(BaseModel):
    id:int
    name:str
    description: str
    price: float
    quantity: int
#this constructor you will use without pydantic
    # def __init__(self, id: int, name: str, description: str, price: float, quantity: int):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.quantity = quantity