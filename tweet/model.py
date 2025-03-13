from sqlalchemy import Column, Integer, String, Boolean, DateTime

from config.models.base import Base


class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    author_id = Column(String, nullable=False)
    inbound = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)
    response_tweet_id = Column(String, nullable=True)
    in_response_to_tweet_id = Column(String, nullable=True)
