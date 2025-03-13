import pandas as pd
from pandas import DataFrame
from sqlalchemy import cast, func, REAL
from sqlalchemy.orm import Session

from models.entity_repository import EntityRepository
from tweet.model import Tweet


class TweetRepository(EntityRepository):
    def __init__(self):
        super().__init__(Tweet)

    def get_one_tweet(self, db_session: Session):
        query = db_session.query(Tweet)
        return self.first(query)

    def get_all(self, db_session: Session) -> DataFrame:
        query = db_session.query(Tweet)
        df = pd.read_sql(query.statement, db_session.bind)
        return df

    def get_by_author_id(self, db_session: Session, author_id: str) -> DataFrame:
        query = db_session.query(Tweet).filter_by(author_id=author_id)
        df = pd.read_sql(query.statement, db_session.bind)
        return df

    def get_tweet_response_rate(self, db_session: Session):
        t_subquery = (
            db_session.query(Tweet.id, Tweet.response_tweet_id)
            .filter(Tweet.response_tweet_id.isnot(None))
            .subquery()
        )
        query = (
            db_session.query(
                cast(
                    func.sum(func.case([(t_subquery.c.id.isnot(None), 1)], else_=0)) / func.count(),
                    REAL,
                ).label("response_ratio")
            )
            .select_from(Tweet)
            .outerjoin(t_subquery, t_subquery.c.response_tweet_id.like("%" + cast(Tweet.tweet_id, REAL) + "%"))
        )
        result = db_session.execute(query).scalar()
        return result
