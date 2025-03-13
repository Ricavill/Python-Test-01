import logging
from typing import List

from sqlalchemy.orm import Query, Session

from config.models.base import Base

#Se creo esta entidad dado que de esta forma podemos tener una manera mas limpia y sin duplicidad de codigo al momento
#de tener errores.
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

    def save_all(self, db: Session, entities: List[Base]) -> List[Base]:
        try:
            db.add_all(entities)
            db.commit()
            return entities
        except Exception as e:
            logging.error(f"Error saving entities {self.entity.__name__}", e)
            db.rollback()
