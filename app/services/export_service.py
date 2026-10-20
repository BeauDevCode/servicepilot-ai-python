import csv
from io import StringIO

from sqlmodel import Session, select

from app.models import Customer, Job


def _spreadsheet_text(value: str | None) -> str:
    text = value or ""
    first = text.lstrip(" \t\r\n")[:1]
    if first in {"=", "+", "-", "@", "＝", "＋", "－", "＠"} or text.startswith(("\t", "\r", "\n")):
        return f"\t{text}"
    return text


def export_customers_csv(session: Session) -> str:
    stream = StringIO()
    writer = csv.writer(stream, quoting=csv.QUOTE_ALL)
    writer.writerow(["Name", "Email", "Phone", "Address", "Status", "Tags"])
    for customer in session.exec(select(Customer)):
        writer.writerow(
            [
                _spreadsheet_text(customer.name),
                _spreadsheet_text(customer.email),
                _spreadsheet_text(customer.phone),
                _spreadsheet_text(customer.address),
                customer.status,
                _spreadsheet_text(customer.tags),
            ]
        )
    return stream.getvalue()


def export_jobs_csv(session: Session) -> str:
    stream = StringIO()
    writer = csv.writer(stream, quoting=csv.QUOTE_ALL)
    writer.writerow(["Title", "Customer ID", "Service", "Status", "Scheduled", "Estimated", "Final"])
    for job in session.exec(select(Job)):
        writer.writerow(
            [
                _spreadsheet_text(job.title),
                job.customer_id,
                _spreadsheet_text(job.service_type),
                job.status,
                job.scheduled_date,
                job.estimated_price,
                job.final_price,
            ]
        )
    return stream.getvalue()

