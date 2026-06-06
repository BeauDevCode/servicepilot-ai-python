import json

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.forms import optional_int
from app.models import Customer, Job, QuoteStatus
from app.services.quote_service import convert_quote_to_invoice, create_quote, get_quote, list_quotes
from app.templating import templates

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.get("")
def quotes_page(request: Request, status: str | None = None, session: Session = Depends(get_session)):
    return templates.TemplateResponse(
        request,
        "quotes.html",
        {
            "active": "quotes",
            "quotes": list_quotes(session, status),
            "customers": list(session.exec(select(Customer))),
            "jobs": list(session.exec(select(Job))),
            "statuses": QuoteStatus,
            "status": status or "",
        },
    )


@router.post("")
def add_quote(
    customer_id: str | None = Form(None),
    job_id: str | None = Form(None),
    description: str = Form(...),
    amount: float = Form(...),
    session: Session = Depends(get_session),
):
    create_quote(
        session,
        customer_id=optional_int(customer_id),
        job_id=optional_int(job_id),
        line_items=json.dumps([{"description": description, "quantity": 1, "unit_price": amount}]),
        subtotal=amount,
        total=amount,
    )
    return RedirectResponse("/quotes", status_code=303)


@router.get("/{quote_id}")
def quote_detail(quote_id: int, request: Request, session: Session = Depends(get_session)):
    quote = get_quote(session, quote_id)
    if not quote:
        raise HTTPException(404)
    return templates.TemplateResponse(request, "quote_detail.html", {"active": "quotes", "quote": quote, "statuses": QuoteStatus})


@router.post("/{quote_id}/convert")
def convert_quote(quote_id: int, session: Session = Depends(get_session)):
    quote = get_quote(session, quote_id)
    if not quote:
        raise HTTPException(404)
    invoice = convert_quote_to_invoice(session, quote)
    return RedirectResponse(f"/invoices/{invoice.id}", status_code=303)
