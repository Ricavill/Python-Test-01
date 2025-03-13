from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.db import get_db

companies_router = APIRouter()


@companies_router.post("/{company_id}/insights")
def insights(db: Session = Depends(get_db)):
    pass