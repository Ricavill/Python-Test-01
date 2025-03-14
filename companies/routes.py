from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.db import get_db
from config.error import NotFoundException
from conversations.conversations_service import ConversationsService
from tweet.tweet_repository import TweetRepository

companies_router = APIRouter()


@companies_router.get("/{company_id}/insights")
def insights(company_id: str, db: Session = Depends(get_db)):
    tweet_repository = TweetRepository()
    # Se buscan todos los tweets por que son pocos, en la vida real si se necesitara solo buscar tweets de compañia se
    # filtraria por compañia en query.
    all_tweets = tweet_repository.get_all(db)
    if all_tweets.empty:
        raise NotFoundException("No tweets found")
    inbound_tweets = all_tweets[(all_tweets["inbound"] == 1)].shape[0]
    outbound_tweets = all_tweets[(all_tweets["inbound"] == 0)].shape[0]
    #Esta seccion en el documento era un poco ambigua, pero se asumo que todo es para el company
    response_rate = tweet_repository.get_tweet_response_rate(db,author_id=company_id)
    conversation_ratio = tweet_repository.get_conversation_ratio(db,author_id=company_id)
    volume_metrics = tweet_repository.get_volume_metrics(db, company_id)
    company_average_response_time = tweet_repository.get_avg_response_time(db, company_id)
    response = {"inbound_tweets": inbound_tweets, "outbound_tweets": outbound_tweets, "response_rate": response_rate,
                "conversation_ratio": conversation_ratio, "volume_metrics": volume_metrics,
                "company_average_response_time_min": company_average_response_time}
    # Se especifica que se muestren el total de inbound y outbounds sin importar la compañia.
    return JSONResponse(status_code=200, content=response)


@companies_router.get("/{company_id}/ai-insights")
def ai_insights(company_id: str, db: Session = Depends(get_db)):
    response = ConversationsService().analyze_company_conversations(db, company_id)
    return response
