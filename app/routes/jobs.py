from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.forms import optional_int
from app.models import Customer, JobStatus, Priority
from app.services.job_service import create_job, get_job, list_jobs, update_job
from app.templating import templates

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
def jobs_page(request: Request, q: str | None = None, status: str | None = None, service_type: str | None = None, session: Session = Depends(get_session)):
    customers = list(session.exec(select(Customer)))
    services = sorted({job.service_type for job in list_jobs(session)})
    return templates.TemplateResponse(
        request,
        "jobs.html",
        {
            "active": "jobs",
            "jobs": list_jobs(session, q, status, service_type),
            "customers": customers,
            "statuses": JobStatus,
            "priorities": Priority,
            "services": services,
            "q": q or "",
            "status": status or "",
            "service_type": service_type or "",
        },
    )


@router.post("")
def add_job(
    customer_id: str | None = Form(None),
    title: str = Form(...),
    description: str = Form(...),
    service_type: str = Form("General Service"),
    status: JobStatus = Form(JobStatus.new),
    priority: Priority = Form(Priority.medium),
    scheduled_date: str | None = Form(None),
    location: str | None = Form(None),
    estimated_price: float = Form(0),
    session: Session = Depends(get_session),
):
    scheduled = datetime.fromisoformat(scheduled_date) if scheduled_date else None
    job = create_job(
        session,
        customer_id=optional_int(customer_id),
        title=title,
        description=description,
        service_type=service_type,
        status=status,
        priority=priority,
        scheduled_date=scheduled,
        location=location,
        estimated_price=estimated_price,
    )
    return RedirectResponse(f"/jobs/{job.id}", status_code=303)


@router.get("/{job_id}")
def job_detail(job_id: int, request: Request, session: Session = Depends(get_session)):
    job = get_job(session, job_id)
    if not job:
        raise HTTPException(404)
    return templates.TemplateResponse(request, "job_detail.html", {"active": "jobs", "job": job, "statuses": JobStatus, "priorities": Priority})


@router.post("/{job_id}")
def edit_job(
    job_id: int,
    status: JobStatus = Form(...),
    priority: Priority = Form(...),
    checklist: str | None = Form(None),
    internal_notes: str | None = Form(None),
    final_price: float = Form(0),
    session: Session = Depends(get_session),
):
    job = get_job(session, job_id)
    if not job:
        raise HTTPException(404)
    update_job(session, job, status=status, priority=priority, checklist=checklist, internal_notes=internal_notes, final_price=final_price)
    return RedirectResponse(f"/jobs/{job_id}", status_code=303)
