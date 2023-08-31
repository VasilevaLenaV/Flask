from sqlite3 import IntegrityError

from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    else:
        return None


def create_user(db: Session, user: schemas.User):
    try:
        hash_pwd = generate_password_hash(user.password)

        db_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email,
                              hashed_password=hash_pwd)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        return e


def update_user(db: Session, user_id: int, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.email = user.email
        db_user.password = user.password
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return None


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


async def get_product(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.id == id)


async def get_products_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name)


def create_product(db: Session, product: schemas.Product):
    try:
        db_product = models.Product(name=product.name, description=product.description, price=product.price)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError as e:
        return e


def update_product(db: Session, product_id: int, product: schemas.Product):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.email = product.price
        db.commit()
        db.refresh(db_product)
        return db_product
    else:
        return None


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    else:
        return None


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders_by_user(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).list()


def get_orders_by_product(db: Session, product_id: int):
    return db.query(models.Order).filter(models.Order.product_id == product_id).list()


def get_orders_by_user_product(db: Session, user_id: int, product_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id and models.Order.product_id == product_id).list()


def create_order(db: Session, order: schemas.Order):
    try:
        db_order = models.Order(user_id=order.user_id,product_id=order.product_id,status=order.status, order_date=order.order_date)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    except IntegrityError as e:
        return e


def update_order(db: Session, order_id: int, order: schemas.Order):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = order.status
        db.commit()
        db.refresh(db_order)
        return db_order
    else:
        return None


def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if db_order:
        db.delete(db_order)
        db.commit()
        return True
    else:
        return None
