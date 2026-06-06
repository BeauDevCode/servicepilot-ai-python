from sqlmodel import Session, SQLModel, create_engine

from app.models import Customer
from app.services.customer_service import create_customer, list_customers


def test_customer_service_creates_and_lists_customer():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        created = create_customer(session, name="Test Customer", email="test@example.com")
        assert created.id is not None
        customers = list_customers(session, q="Test")
        assert len(customers) == 1
        assert isinstance(customers[0], Customer)

