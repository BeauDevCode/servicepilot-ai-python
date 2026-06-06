import json
from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.database import get_session
from app.models import Priority
from app.services import customer_service, job_service, quote_service, task_service
from app.services.ai_service import extract_request
from app.templating import templates

router = APIRouter(prefix="/ai-assistant", tags=["ai"])

DEFAULT_MESSAGE = "hey bro can you come saturday to fix my brakes i got a 2008 honda accord and it making grinding sound how much"


@router.get("")
def ai_page(request: Request):
    return templates.TemplateResponse("ai_assistant.html", {"request": request, "active": "ai", "message": DEFAULT_MESSAGE, "result": None})


@router.post("")
async def analyze_message(request: Request, message: str = Form(...)):
    result = await extract_request(message)
    return templates.TemplateResponse("ai_assistant.html", {"request": request, "active": "ai", "message": message, "result": result})


@router.post("/create-workflow")
async def create_workflow(message: str = Form(...), session: Session = Depends(get_session)):
    result = await extract_request(message)
    customer = customer_service.create_customer(
        session,
        name=result.customer_name or "New Lead",
        email=result.email,
        phone=result.phone,
        address=result.location,
        notes=f"Created from AI intake.\n\nOriginal message:\n{message}",
        tags=result.service_category,
    )
    job = job_service.create_job(
        session,
        customer_id=customer.id,
        title=result.job_title,
        description=result.job_description,
        service_type=result.service_category,
        priority=Priority.high if result.urgency == "High" else Priority.medium,
        location=result.location,
        checklist="\n".join(result.suggested_checklist),
        estimated_price=result.suggested_quote_high,
        source_message=message,
    )
    quote_service.quote_from_job(session, job.id, customer.id, result.suggested_quote_low, result.suggested_quote_high)
    task_service.create_task(
        session,
        title=f"Follow up with {customer.name}",
        description=result.follow_up_message,
        customer_id=customer.id,
        job_id=job.id,
        due_date=date.today(),
        priority=Priority.high if result.missing_information else Priority.medium,
    )
    return RedirectResponse(f"/jobs/{job.id}", status_code=303)


@router.post("/api/extract")
async def extract_api(message: str = Form(...)):
    result = await extract_request(message)
    return json.loads(result.model_dump_json())
