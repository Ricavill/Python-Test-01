from fastapi import FastAPI
from config.logging import LoggingMiddleware
from companies.routes import companies_router
from config.auth.auth_middleware import AuthMiddleware
from config.db import init_db
from config.error import init_error_handlers
from llm.llama import Llama
from tweet.routes import tweets_router
from user.routes import users_router

app = FastAPI(openapi_url="/api/v1/openapi.json",docs_url="/documentation", redoc_url=None)
#Se añade middleware para guardar en log requests, responses.
app.add_middleware(LoggingMiddleware)
#Se añade middleware para authenticar bearer token
app.add_middleware(AuthMiddleware)
#Se inicializa base de datos
init_db()
#Se inicializan error handlers
init_error_handlers(app)
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(tweets_router, prefix="/api/tweets", tags=["Tweets"])
app.include_router(companies_router, prefix="/api/companies", tags=["Companies"])



@app.get("/")
def read_root():
    return {"Hello": "World"}
