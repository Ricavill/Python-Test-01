import kagglehub
import pandas as pd
from fastapi import APIRouter, Depends
from kagglehub import KaggleDatasetAdapter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.db import get_db
from tweet.model import Tweet
from tweet.tweet_repository import TweetRepository

tweets_router = APIRouter()


@tweets_router.post("/ingest")
def ingest(db: Session = Depends(get_db)):
    tweet_repository = TweetRepository()
    # Se busca por lo menos un tweet para saber si ya se guardaron los tweets de esta base de datos.
    # Solo se usara este metodo de evitar un nuevo ingest solo en este ejercicio dado que se sabe que el
    # dataset no cambiara, en la vida real se usarian otras tecnicas para verificar que el bulk creation
    # no este registrando tweets duplicados, como busqueda de tweets por tweets ids y luego validar que no
    # existan para crearlos.
    tweet = tweet_repository.get_one_tweet(db)
    if tweet:
        return JSONResponse(status_code=200, content={'message': "Ingest already Completed"})
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "thoughtvector/customer-support-on-twitter",
        "sample.csv")
    df = df.where(pd.notna(df), None)
    df['created_at'] = pd.to_datetime(df['created_at'], format="%a %b %d %H:%M:%S %z %Y")
    tweets = []
    for tweet in df.iterrows():
        if len(tweet) > 1:
            tweet = Tweet().create(dict(tweet[1]))
            tweets.append(tweet)
    if tweets:
        tweet_repository.save_all(db, tweets)
    return JSONResponse(status_code=200, content={'message': "Ingest Completed"})
