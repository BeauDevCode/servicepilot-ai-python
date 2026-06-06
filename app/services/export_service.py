import csv
from io import StringIO

from sqlmodel import Session, select

from app.models import Customer, Job


def export_customers_csv(session: Session) -> str:
    stream = StringIO()
    writer = csv.writer(stream)
    writer.writerow(["Name", "Email", "Phone", "Address", "Status", "Tags"])
    for customer in session.exec(select(Customer)):
        writer.writerow([customer.name, customer.email, customer.phone, customer.address, customer.status, customer.tags])
    return stream.getvalue()


def export_jobs_csv(session: Session) -> str:
    stream = StringIO()
    writer = csv.writer(stream)
    writer.writerow(["Title", "Customer ID", "Service", "Status", "Scheduled", "Estimated", "Final"])
    for job in session.exec(select(Job)):
        writer.writerow([job.title, job.customer_id, job.service_type, job.status, job.scheduled_date, job.estimated_price, job.final_price])
    return stream.getvalue()

