from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

from app.database import get_session
from app.services.export_service import export_customers_csv, export_jobs_csv

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/exports/customers.csv")
def customers_csv(session: Session = Depends(get_session)):
    return Response(export_customers_csv(session), media_type="text/csv")


@router.get("/exports/jobs.csv")
def jobs_csv(session: Session = Depends(get_session)):
    return Response(export_jobs_csv(session), media_type="text/csv")

