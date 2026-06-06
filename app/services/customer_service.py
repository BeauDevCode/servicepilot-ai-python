from sqlmodel import Session, col, func, select

from app.models import Customer


def list_customers(session: Session, q: str | None = None, status: str | None = None) -> list[Customer]:
    statement = select(Customer).order_by(col(Customer.created_at).desc())
    if q:
        statement = statement.where(Customer.name.contains(q) | Customer.email.contains(q) | Customer.phone.contains(q))
    if status:
        statement = statement.where(Customer.status == status)
    return list(session.exec(statement))


def get_customer(session: Session, customer_id: int) -> Customer | None:
    return session.get(Customer, customer_id)


def create_customer(session: Session, **data: object) -> Customer:
    customer = Customer(**data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


def customer_lifetime_value(session: Session, customer_id: int) -> float:
    from app.models import Invoice, InvoiceStatus

    return session.exec(
        select(func.coalesce(func.sum(Invoice.total), 0)).where(Invoice.customer_id == customer_id, Invoice.status == InvoiceStatus.paid)
    ).one()

