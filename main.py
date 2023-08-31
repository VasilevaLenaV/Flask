from typing import List

from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.db_init import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException

from db.models import Product, Order, User

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products/", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product = crud.get_products_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already created")
    return crud.create_product(db=db, product=product)


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.Product, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id, product)

    if db_product is None:
        raise HTTPException(status_code=400, detail="Product not found")
    return db_product


@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db, product_id)

    if db_product is None:
        raise HTTPException(status_code=400, detail="Product not found")
    return db_product


@app.get("/orders/", response_model=list[schemas.Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_orders = crud.get_orders(db, skip=skip, limit=limit)
    return db_orders


@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int,db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.Order, db: Session = Depends(get_db)):
    db_order = crud.get_orders_by_user_product(db, order.user_id,order.product_id)
    if db_order:
        raise HTTPException(status_code=400, detail="Order already created")
    return crud.create_order(db=db, order=db_order)


@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.Order,db: Session = Depends(get_db)):
    db_order = crud.update_order(db, order_id, order)

    if db_order is None:
        raise HTTPException(status_code=400, detail="Order not found")
    return db_order


@app.delete("/orders/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id)

    if db_order is None:
        raise HTTPException(status_code=400, detail="Order not found")
    return db_order



@app.get("/users", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = crud.get_users(db, skip=skip, limit=limit)
    return db_users


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int,db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already created")
    return crud.create_user(db=db, user=db_user)


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.User,db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Order not found")
    return db_user



@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    response = crud.delete_user(db, user_id)

    if response is None:
        raise HTTPException(status_code=400, detail="User not found")
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
