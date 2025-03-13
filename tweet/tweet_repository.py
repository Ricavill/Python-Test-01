from sqlalchemy.orm import Session

from models.entity_repository import EntityRepository
from tweet.model import Tweet


class TweetRepository(EntityRepository):
    def __init__(self):
        super().__init__(Tweet)

    def get_one_tweet(self, db_session: Session):
        query = db_session.query(Tweet)
        return self.first(query)
