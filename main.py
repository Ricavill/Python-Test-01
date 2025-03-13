from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.auth.__init import user_login
from config.auth.jwt_middleware import JWTMiddleware
from config.db import init_db, get_db
from config.error import init_error_handlers
from tweet.routes import tweet_router
from user.routes import user_router

app = FastAPI()
app.add_middleware(JWTMiddleware)
init_db()
init_error_handlers(app)
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(tweet_router, prefix="/api/tweets", tags=["Tweets"])


@app.get("/")
def read_root():
    return {"Hello": "World"}

