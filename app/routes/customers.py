from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.models import CustomerStatus, Invoice, Job, Quote, Task
from app.services.customer_service import create_customer, customer_lifetime_value, get_customer, list_customers
from app.templating import templates

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("")
def customers_page(request: Request, q: str | None = None, status: str | None = None, session: Session = Depends(get_session)):
    return templates.TemplateResponse(
        request,
        "customers.html",
        {"active": "customers", "customers": list_customers(session, q, status), "statuses": CustomerStatus, "q": q or "", "status": status or ""},
    )


@router.post("")
def add_customer(
    name: str = Form(...),
    email: str | None = Form(None),
    phone: str | None = Form(None),
    address: str | None = Form(None),
    notes: str | None = Form(None),
    tags: str | None = Form(None),
    session: Session = Depends(get_session),
):
    create_customer(session, name=name, email=email, phone=phone, address=address, notes=notes, tags=tags)
    return RedirectResponse("/customers", status_code=303)


@router.get("/{customer_id}")
def customer_detail(customer_id: int, request: Request, session: Session = Depends(get_session)):
    customer = get_customer(session, customer_id)
    if not customer:
        raise HTTPException(404)
    return templates.TemplateResponse(
        request,
        "customer_detail.html",
        {
            "active": "customers",
            "customer": customer,
            "jobs": list(session.exec(select(Job).where(Job.customer_id == customer_id))),
            "quotes": list(session.exec(select(Quote).where(Quote.customer_id == customer_id))),
            "invoices": list(session.exec(select(Invoice).where(Invoice.customer_id == customer_id))),
            "tasks": list(session.exec(select(Task).where(Task.customer_id == customer_id))),
            "lifetime_value": customer_lifetime_value(session, customer_id),
        },
    )
