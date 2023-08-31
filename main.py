from fastapi import Depends, FastAPI, HTTPException, Request, Body, Form
from pydantic_core import PydanticUndefined
from sqlalchemy.orm import Session
from starlette import status
from starlette.datastructures import URL
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from typing import Annotated

from db import crud, models, schemas
from db.db_init import SessionLocal, engine
from form import UserForm
from pydantic import BaseModel, Field

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    username: str = Form()
    email: str = Form()
    password: str = Form()


users: list[User] = []


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_users(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), msg: str = None):
    users_ = crud.get_users(db, skip=skip, limit=limit)

    context = {'request': request, 'users': users_, "msg": msg}
    return templates.TemplateResponse("users.html", context=context, status_code=200)


@app.get("/users", response_class=HTMLResponse)
async def list_users(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/create", response_class=HTMLResponse)
async def add_user(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("create.html", {"request": request, "user": User})


@app.post("/users/create", response_class=RedirectResponse)
async def create_users(request: Request, db: Session = Depends(get_db)):
    user = UserForm(request)
    await user.load_data()

    if await user.is_valid():
        db_user = await crud.get_user_by_email(db, email=user.email)
        if db_user is None:
            try:
                user_, err = crud.create_user(db=db, user=user)
                if user_:
                    user.__dict__.update(message="User created")
                else:
                    user.__dict__.get("errors").append(err)
                return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            except HTTPException:
                user.__dict__.update(message="")
                user.__dict__.get("errors").append("Incorrect Email or Password")
                return "/users/create"
        else:
            raise HTTPException(status_code=400, detail="Email already registered")
    return "/"


@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    response = crud.delete_user(db, user_id=user_id)

    if response:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
    response = crud.update_user(db, user_id, user)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")
    return response


@app.post("/users/", status_code=status.HTTP_200_OK)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
