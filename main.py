from fastapi import FastAPI

from config.logging import LoggingMiddleware
from config.auth.auth_middleware import AuthMiddleware
from config.db import init_db
from config.error import init_error_handlers
from tweet.routes import tweet_router
from user.routes import user_router

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)
init_db()
init_error_handlers(app)
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(tweet_router, prefix="/api/tweets", tags=["Tweets"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
