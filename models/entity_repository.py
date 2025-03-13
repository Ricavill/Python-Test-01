import logging

from sqlalchemy.orm import Query, Session

from config.models.base import Base


class EntityRepository:
    def __init__(self, entity: Base):
        self.entity = entity

    def first(self, query: Query):
        try:
            return query.first()
        except Exception as e:
            logging.error(f"Exception while getting {self.entity.__name__}: {e}")

    def all(self, query: Query):
        try:
            return query.all()
        except Exception as e:
            logging.error(f"Exception while getting {self.entity.__name__}: {e}")

    def save(self, db: Session, entity: Base) -> Base:
        try:
            db.add(entity)
            db.commit()
            return entity
        except Exception as e:
            logging.error(f"Error saving {self.entity.__name__}", e)
            db.rollback()
