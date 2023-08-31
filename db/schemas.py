from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    status: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
