from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.auth.__init import user_login
from config.db import get_db

users_router = APIRouter()


@users_router.post("/login")
def login(user: dict, db: Session = Depends(get_db)):
    token = user_login(db, user)
    if token:
        return JSONResponse(status_code=200, content={'token': token})
    else:
        return JSONResponse(status_code=401, content={'status': "Invalid Credentials"})
