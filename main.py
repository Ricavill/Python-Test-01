from fastapi import FastAPI

from companies.routes import companies_router
from config.logging import LoggingMiddleware
from config.auth.auth_middleware import AuthMiddleware
from config.db import init_db
from config.error import init_error_handlers
from llm.llama import Llama
from tweet.routes import tweets_router
from user.routes import users_router

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)
init_db()
init_error_handlers(app)
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(tweets_router, prefix="/api/tweets", tags=["Tweets"])
app.include_router(companies_router, prefix="/api/companies", tags=["Companies"])



@app.get("/")
def read_root():
    return {"Hello": "World"}
