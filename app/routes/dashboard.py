from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, col, select

from app.database import get_session
from app.models import Invoice, Job, Quote
from app.services.analytics_service import dashboard_stats
from app.templating import templates

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def dashboard(request: Request, session: Session = Depends(get_session)):
    stats = dashboard_stats(session)
    recent_jobs = list(session.exec(select(Job).order_by(col(Job.created_at).desc()).limit(5)))
    upcoming_jobs = list(session.exec(select(Job).where(Job.scheduled_date != None).order_by(col(Job.scheduled_date)).limit(5)))  # noqa: E711
    recent_quotes = list(session.exec(select(Quote).order_by(col(Quote.created_at).desc()).limit(4)))
    invoices = list(session.exec(select(Invoice).order_by(col(Invoice.created_at).desc()).limit(4)))
    suggestions = [
        "Follow up with Marcus about unpaid invoice #1003.",
        "Quote for apartment deep clean is still pending.",
        "You have jobs without scheduled dates.",
        "Send a review request to completed customers.",
    ]
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "active": "dashboard",
            "stats": stats,
            "recent_jobs": recent_jobs,
            "upcoming_jobs": upcoming_jobs,
            "recent_quotes": recent_quotes,
            "invoices": invoices,
            "suggestions": suggestions,
        },
    )
