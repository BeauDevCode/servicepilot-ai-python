from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from app.database import get_session
from app.services.analytics_service import analytics_summary
from app.templating import templates

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("")
def analytics_page(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("analytics.html", {"request": request, "active": "analytics", "summary": analytics_summary(session)})
