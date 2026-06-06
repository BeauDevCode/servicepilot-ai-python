from sqlmodel import Session, SQLModel, create_engine

from app.models import Customer, Invoice, InvoiceStatus, Priority
from app.services.analytics_service import analytics_summary, dashboard_stats
from app.services.customer_service import create_customer, list_customers
from app.services.invoice_service import mark_paid
from app.services.job_service import create_job
from app.services.quote_service import quote_from_job
from app.services.task_service import complete_task, create_task


def test_customer_service_creates_and_lists_customer():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        created = create_customer(session, name="Test Customer", email="test@example.com")
        assert created.id is not None
        customers = list_customers(session, q="Test")
        assert len(customers) == 1
        assert isinstance(customers[0], Customer)


def test_job_quote_invoice_task_and_analytics_services():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        customer = create_customer(session, name="Workflow Customer", email="workflow@example.com")
        job = create_job(
            session,
            customer_id=customer.id,
            title="Brake repair",
            description="Grinding brake noise",
            service_type="Mobile Mechanic",
            estimated_price=300,
        )
        quote = quote_from_job(session, job.id, customer.id, 200, 400)
        invoice = Invoice(
            invoice_number="INV-T",
            customer_id=customer.id,
            job_id=job.id,
            quote_id=quote.id,
            subtotal=quote.subtotal,
            total=quote.total,
            status=InvoiceStatus.sent,
        )
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        task = create_task(session, title="Follow up", customer_id=customer.id, job_id=job.id, priority=Priority.high)

        assert quote.total == 300
        assert invoice.balance_due == 300
        assert complete_task(session, task.id).completed is True
        assert mark_paid(session, invoice).balance_due == 0
        assert dashboard_stats(session).total_customers == 1
        assert analytics_summary(session)["paid_invoices"] == 1
