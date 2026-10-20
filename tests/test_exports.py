import csv
from io import StringIO

from sqlmodel import Session, SQLModel, create_engine

from app.models import Customer, Job
from app.services.export_service import export_customers_csv, export_jobs_csv


def test_customer_export_preserves_fields_and_disarms_spreadsheet_formulas():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Customer(name='=HYPERLINK("https://example.invalid","Open")', email="safe@example.com", tags='urgent, "today"'))
        session.commit()

        exported = export_customers_csv(session)
        rows = list(csv.reader(StringIO(exported)))

    assert '"\t=HYPERLINK' in exported
    assert rows[0] == ["Name", "Email", "Phone", "Address", "Status", "Tags"]
    assert rows[1] == ['\t=HYPERLINK("https://example.invalid","Open")', "safe@example.com", "", "", "Active", 'urgent, "today"']


def test_job_export_disarms_formula_in_user_entered_title():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Job(title=" +SUM(1,2)", description="A test job", service_type="Repair"))
        session.commit()

        rows = list(csv.reader(StringIO(export_jobs_csv(session))))

    assert rows[0] == ["Title", "Customer ID", "Service", "Status", "Scheduled", "Estimated", "Final"]
    assert rows[1][0] == "\t +SUM(1,2)"
    assert rows[1][2:4] == ["Repair", "New"]
