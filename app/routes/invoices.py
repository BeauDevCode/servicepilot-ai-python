import json
from datetime import date

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.models import Customer, InvoiceStatus, Job
from app.services.invoice_service import create_invoice, get_invoice, list_invoices, mark_paid
from app.templating import templates

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("")
def invoices_page(request: Request, status: str | None = None, session: Session = Depends(get_session)):
    return templates.TemplateResponse(
        "invoices.html",
        {
            "request": request,
            "active": "invoices",
            "invoices": list_invoices(session, status),
            "customers": list(session.exec(select(Customer))),
            "jobs": list(session.exec(select(Job))),
            "statuses": InvoiceStatus,
            "status": status or "",
        },
    )


@router.post("")
def add_invoice(customer_id: int | None = Form(None), job_id: int | None = Form(None), description: str = Form(...), amount: float = Form(...), session: Session = Depends(get_session)):
    create_invoice(
        session,
        customer_id=customer_id,
        job_id=job_id,
        line_items=json.dumps([{"description": description, "quantity": 1, "unit_price": amount}]),
        subtotal=amount,
        total=amount,
        due_date=date.today(),
        status=InvoiceStatus.sent,
    )
    return RedirectResponse("/invoices", status_code=303)


@router.get("/{invoice_id}")
def invoice_detail(invoice_id: int, request: Request, session: Session = Depends(get_session)):
    invoice = get_invoice(session, invoice_id)
    if not invoice:
        raise HTTPException(404)
    return templates.TemplateResponse("invoice_detail.html", {"request": request, "active": "invoices", "invoice": invoice})


@router.post("/{invoice_id}/paid")
def pay_invoice(invoice_id: int, session: Session = Depends(get_session)):
    invoice = get_invoice(session, invoice_id)
    if not invoice:
        raise HTTPException(404)
    mark_paid(session, invoice)
    return RedirectResponse(f"/invoices/{invoice_id}", status_code=303)
