from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Float,DateTime
from sqlalchemy.orm import relationship, Mapped

from .db_init import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, unique=False, index=True)
    price = Column(Float)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    userItem: Mapped["UserItem"] = relationship("User", backref="users")
    product_id = Column(Integer, ForeignKey("products.id"))
    productItem: Mapped["ProductItem"] = relationship("Product", backref="products")
    order_date = Column(DateTime, index=True)
    status = Column(String)

