from sqlmodel import Session, col, select

from app.models import Invoice, InvoiceStatus


def next_invoice_number(session: Session) -> str:
    count = len(list(session.exec(select(Invoice.id))))
    return f"INV-{1001 + count}"


def list_invoices(session: Session, status: str | None = None) -> list[Invoice]:
    statement = select(Invoice).order_by(col(Invoice.created_at).desc())
    if status:
        statement = statement.where(Invoice.status == status)
    return list(session.exec(statement))


def create_invoice(session: Session, **data: object) -> Invoice:
    data.setdefault("invoice_number", next_invoice_number(session))
    invoice = Invoice(**data)
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice


def get_invoice(session: Session, invoice_id: int) -> Invoice | None:
    return session.get(Invoice, invoice_id)


def mark_paid(session: Session, invoice: Invoice) -> Invoice:
    invoice.amount_paid = invoice.total
    invoice.status = InvoiceStatus.paid
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice

