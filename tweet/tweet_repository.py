from typing import List

import pandas as pd
from pandas import DataFrame
from sqlalchemy import func, case, cast, Float
from sqlalchemy.orm import Session, aliased

from models.entity_repository import EntityRepository
from tweet.model import Tweet


class TweetRepository(EntityRepository):
    def __init__(self):
        super().__init__(Tweet)

    def get_one_tweet(self, db_session: Session):
        query = db_session.query(Tweet)
        return self.first(query)

    def get_all_orm(self, db_session: Session) -> DataFrame:
        query = db_session.query(Tweet)
        return self.all(query)

    def get_all(self, db_session: Session) -> DataFrame:
        query = db_session.query(Tweet)
        df = pd.read_sql(query.statement, db_session.bind)
        return df

    def get_all_responded_tweets(self, db: Session) -> List[Tweet]:
        query = db.query(Tweet).filter(Tweet.in_response_to_tweet_id.is_(None))
        return query

    def get_by_author_id(self, db_session: Session, author_id: str) -> DataFrame:
        query = db_session.query(Tweet).filter_by(author_id=author_id)
        df = pd.read_sql(query.statement, db_session.bind)
        return df

    def get_tweets_sent_to_author(self, db_session: Session, author_id: str):
        #Se definen aliases por que sino no hay como diferenciar una tabla de otra.
        t1 = aliased(Tweet)
        t2 = aliased(Tweet)
        query =  db_session.query(t1).filter(
            t1.inbound.is_(True),
            t1.in_response_to_tweet_id.isnot(None)  # Ensure it's a reply
        ).join(t2, t1.tweet_id == t2.in_response_to_tweet_id).filter(
            t2.author_id == author_id, t2.inbound==0
        )
        return self.all(query)

    def get_tweet_response_rate(self, db_session: Session):
        t1 = aliased(Tweet)
        t2 = aliased(Tweet)

        stmt = db_session.query(
            (func.count(func.distinct(t1.id)) * 100.0 / func.count(func.distinct(t2.id))).label("response_rate")
        ).select_from(t1).outerjoin(
            t2, t1.in_response_to_tweet_id == t2.tweet_id
        ).filter(t2.inbound == True)

        result = db_session.execute(stmt).scalar()
        return result or 0

    def get_conversation_ratio(self, db_session: Session):
        t1 = aliased(Tweet)
        t2 = aliased(Tweet)

        stmt = db_session.query(
            (func.count(t1.id) * 1.0 / func.count(t2.id)).label("response_ratio")
        ).select_from(t1).join(
            t2, t1.in_response_to_tweet_id == t2.tweet_id
        ).filter(
            t1.inbound == 0,
            t2.inbound == 1
        )

        result = db_session.execute(stmt).scalar()
        return result or 0

    def get_volume_metrics(self, db_session: Session, company_id: str):
        stmt = db_session.query(
            (
                    func.sum(case((Tweet.response_tweet_id.isnot(None), 1), else_=0)) * 100.0 /
                    func.sum(case((Tweet.in_response_to_tweet_id.isnot(None), 1), else_=0))
            ).label("response_rate")
        ).filter(Tweet.author_id == company_id, Tweet.inbound == 0)

        result = db_session.execute(stmt).scalar()
        return result or 0

    def get_avg_response_time(self, db_session: Session, company_id: str):
        t1 = aliased(Tweet)
        t2 = aliased(Tweet)

        stmt = db_session.query(
            func.avg(
                (cast(func.strftime('%s', t1.created_at), Float) - cast(func.strftime('%s', t2.created_at),
                                                                        Float)) / 60.0
            ).label("avg_response_time_minutes")
        ).select_from(t1).join(
            t2, t1.in_response_to_tweet_id == t2.tweet_id
        ).filter(
            t1.inbound == False,
            t1.author_id == company_id,
            t2.inbound == True
        )

        result = db_session.execute(stmt).scalar()
        return result or 0
