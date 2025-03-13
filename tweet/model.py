from sqlalchemy import Column, Integer, String, Boolean, DateTime

from config.error import ValidationException
from config.models.base import Base


class Tweet(Base):
    __tablename__ = 'tweet'
    creation_fields = ['tweet_id', 'author_id', "inbound", "created_at", "text", "response_tweet_id",
                       "in_response_to_tweet_id"]
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # Se tendra un id de la tabla Tweet propia de JelouAI y otro para el tweet de la base Kagle para poder
    # diferenciarlos, dado que nuestra entidad Tweet no debe ser una copia exacta del suyo. En nuestra base podremos
    # agregar otros datos que no tiene twitter que a nosotros nos resultarian utiles.
    tweet_id = Column(Integer, nullable=False)
    author_id = Column(String, nullable=False)
    inbound = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)
    response_tweet_id = Column(Integer, nullable=True)
    in_response_to_tweet_id = Column(Integer, nullable=True)

    def setattr_from_data(self, data: dict):
        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])

    def create(self, tweet_data: dict):
        if not tweet_data:
            return None
        required_fields = set(self.creation_fields) - set(tweet_data.keys())
        if len(required_fields) != 0:
            raise ValidationException(f"Required fields: {required_fields}")
        self.setattr_from_data(tweet_data)
        return self
