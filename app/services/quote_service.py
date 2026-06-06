import json

from sqlmodel import Session, col, select

from app.models import Invoice, InvoiceStatus, Quote, QuoteStatus


def next_quote_number(session: Session) -> str:
    count = len(list(session.exec(select(Quote.id))))
    return f"Q-{1001 + count}"


def create_quote(session: Session, **data: object) -> Quote:
    data.setdefault("quote_number", next_quote_number(session))
    quote = Quote(**data)
    session.add(quote)
    session.commit()
    session.refresh(quote)
    return quote


def list_quotes(session: Session, status: str | None = None) -> list[Quote]:
    statement = select(Quote).order_by(col(Quote.created_at).desc())
    if status:
        statement = statement.where(Quote.status == status)
    return list(session.exec(statement))


def get_quote(session: Session, quote_id: int) -> Quote | None:
    return session.get(Quote, quote_id)


def quote_from_job(session: Session, job_id: int, customer_id: int | None, low: float, high: float) -> Quote:
    total = round((low + high) / 2, 2)
    items = [{"description": "Service labor and materials estimate", "quantity": 1, "unit_price": total}]
    return create_quote(
        session,
        customer_id=customer_id,
        job_id=job_id,
        line_items=json.dumps(items),
        subtotal=total,
        tax=0,
        total=total,
        status=QuoteStatus.draft,
        notes="AI-assisted draft. Review scope, taxes, and final pricing before sending.",
    )


def convert_quote_to_invoice(session: Session, quote: Quote) -> Invoice:
    from app.services.invoice_service import next_invoice_number

    invoice = Invoice(
        invoice_number=next_invoice_number(session),
        customer_id=quote.customer_id,
        job_id=quote.job_id,
        quote_id=quote.id,
        line_items=quote.line_items,
        subtotal=quote.subtotal,
        tax=quote.tax,
        total=quote.total,
        amount_paid=0,
        status=InvoiceStatus.sent,
    )
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice

