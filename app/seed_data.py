import json
from datetime import UTC, date, datetime, timedelta

from sqlmodel import Session, select

from app.database import engine
from app.models import BusinessSettings, Customer, Invoice, InvoiceStatus, Job, JobStatus, Priority, Quote, QuoteStatus, Task


def seed_demo_data() -> None:
    with Session(engine) as session:
        if session.exec(select(Customer)).first():
            return

        customers = [
            Customer(name="Marcus Johnson", email="marcus@example.com", phone="(312) 555-1001", address="West Loop, Chicago", tags="mobile mechanic", notes="Prefers text updates."),
            Customer(name="Tanya Rivera", email="tanya@example.com", phone="(312) 555-1002", address="Logan Square, Chicago", tags="cleaning, pets", notes="Two-bedroom apartment with pets."),
            Customer(name="Avery Chen", email="avery@example.com", phone="(312) 555-1003", address="Oak Park, IL", tags="photography", notes="Interested in graduation photos."),
            Customer(name="Jordan Ellis", email="jordan@example.com", phone="(312) 555-1004", address="Evanston, IL", tags="landscaping", notes="Recurring lawn care lead."),
        ]
        session.add_all(customers)
        session.commit()
        for customer in customers:
            session.refresh(customer)

        jobs = [
            Job(customer_id=customers[0].id, title="Brake inspection for Honda Accord", description="Grinding sound when braking on a 2008 Honda Accord.", service_type="Mobile Mechanic", status=JobStatus.scheduled, priority=Priority.high, scheduled_date=datetime.now(UTC) + timedelta(days=2), location=customers[0].address, checklist="Confirm vehicle details\nInspect pads and rotors\nPrepare parts estimate", estimated_price=320),
            Job(customer_id=customers[1].id, title="Two-bedroom deep clean", description="Apartment deep clean with pets in the home.", service_type="Cleaning", status=JobStatus.quoted, priority=Priority.medium, scheduled_date=datetime.now(UTC) + timedelta(days=5), location=customers[1].address, checklist="Confirm parking\nBring pet-safe products\nDeep clean kitchen and bath", estimated_price=240),
            Job(customer_id=customers[2].id, title="Graduation portrait session", description="Outdoor portrait package with edited gallery.", service_type="Photography", status=JobStatus.completed, priority=Priority.medium, scheduled_date=datetime.now(UTC) - timedelta(days=8), location=customers[2].address, estimated_price=450, final_price=450),
            Job(customer_id=customers[3].id, title="Spring yard cleanup", description="Mulch, trimming, and lawn cleanup.", service_type="Landscaping", status=JobStatus.needs_info, priority=Priority.low, location=customers[3].address, estimated_price=275),
        ]
        session.add_all(jobs)
        session.commit()
        for job in jobs:
            session.refresh(job)

        def line(desc: str, amount: float) -> str:
            return json.dumps([{"description": desc, "quantity": 1, "unit_price": amount}])
        quotes = [
            Quote(quote_number="Q-1001", customer_id=customers[1].id, job_id=jobs[1].id, line_items=line("Deep clean package", 240), subtotal=240, total=240, status=QuoteStatus.sent, notes="Includes pet hair detail work."),
            Quote(quote_number="Q-1002", customer_id=customers[3].id, job_id=jobs[3].id, line_items=line("Spring cleanup estimate", 275), subtotal=275, total=275, status=QuoteStatus.draft),
        ]
        invoices = [
            Invoice(invoice_number="INV-1001", customer_id=customers[2].id, job_id=jobs[2].id, line_items=line("Graduation portrait session", 450), subtotal=450, tax=0, total=450, amount_paid=450, due_date=date.today() - timedelta(days=5), status=InvoiceStatus.paid),
            Invoice(invoice_number="INV-1003", customer_id=customers[0].id, job_id=jobs[0].id, line_items=line("Brake diagnostic deposit", 95), subtotal=95, tax=0, total=95, amount_paid=0, due_date=date.today() - timedelta(days=2), status=InvoiceStatus.overdue),
        ]
        tasks = [
            Task(title="Send Tanya quote reminder", description="Ask whether Friday afternoon still works.", customer_id=customers[1].id, job_id=jobs[1].id, due_date=date.today(), priority=Priority.medium),
            Task(title="Call Marcus about invoice #1003", description="Friendly reminder for diagnostic deposit.", customer_id=customers[0].id, job_id=jobs[0].id, due_date=date.today() - timedelta(days=1), priority=Priority.high),
            Task(title="Ask Avery for a review", description="Completed customer review request.", customer_id=customers[2].id, job_id=jobs[2].id, due_date=date.today() + timedelta(days=1), priority=Priority.low),
        ]
        session.add_all(quotes + invoices + tasks + [BusinessSettings()])
        session.commit()
