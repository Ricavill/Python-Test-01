from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.db import get_db
from config.error import NotFoundException
from tweet.tweet_repository import TweetRepository

companies_router = APIRouter()


@companies_router.post("/{company_id}/insights")
def insights(company_id: str, db: Session = Depends(get_db)):
    tweet_repository = TweetRepository()
    # Se buscan todos los tweets por que son pocos, en la vida real si se necesitara solo buscar tweets de compañia se
    # filtraria por compañia en query.
    all_tweets = tweet_repository.get_all(db)
    if all_tweets.empty:
        raise NotFoundException("No tweets found")
    inbound_tweets = all_tweets[(all_tweets["inbound"] == 1)].shape[0]
    outbound_tweets = all_tweets[(all_tweets["inbound"] == 0)].shape[0]
    response_rate = tweet_repository.get_tweet_response_rate(db)
    # Se especifica que se muestren el total de inbound y outbounds sin importar la compañia.
    return JSONResponse(status_code=200, content=response)
