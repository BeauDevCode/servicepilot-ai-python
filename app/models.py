from datetime import date, datetime
from enum import Enum

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel


class CustomerStatus(str, Enum):
    active = "Active"
    prospect = "Prospect"
    inactive = "Inactive"


class JobStatus(str, Enum):
    new = "New"
    needs_info = "Needs Info"
    quoted = "Quoted"
    scheduled = "Scheduled"
    in_progress = "In Progress"
    completed = "Completed"
    cancelled = "Cancelled"


class QuoteStatus(str, Enum):
    draft = "Draft"
    sent = "Sent"
    accepted = "Accepted"
    declined = "Declined"
    expired = "Expired"


class InvoiceStatus(str, Enum):
    draft = "Draft"
    sent = "Sent"
    paid = "Paid"
    overdue = "Overdue"
    cancelled = "Cancelled"


class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    urgent = "Urgent"


class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    status: CustomerStatus = CustomerStatus.active
    notes: str | None = Field(default=None, sa_column=Column(Text))
    tags: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    jobs: list["Job"] = Relationship(back_populates="customer")
    quotes: list["Quote"] = Relationship(back_populates="customer")
    invoices: list["Invoice"] = Relationship(back_populates="customer")
    tasks: list["Task"] = Relationship(back_populates="customer")


class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int | None = Field(default=None, foreign_key="customer.id")
    title: str
    description: str = Field(sa_column=Column(Text))
    service_type: str = "General Service"
    status: JobStatus = JobStatus.new
    priority: Priority = Priority.medium
    scheduled_date: datetime | None = None
    location: str | None = None
    internal_notes: str | None = Field(default=None, sa_column=Column(Text))
    checklist: str | None = Field(default=None, sa_column=Column(Text))
    estimated_price: float = 0
    final_price: float = 0
    source_message: str | None = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    customer: Customer | None = Relationship(back_populates="jobs")
    quotes: list["Quote"] = Relationship(back_populates="job")
    invoices: list["Invoice"] = Relationship(back_populates="job")
    tasks: list["Task"] = Relationship(back_populates="job")


class Quote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quote_number: str
    customer_id: int | None = Field(default=None, foreign_key="customer.id")
    job_id: int | None = Field(default=None, foreign_key="job.id")
    line_items: str = Field(default="[]", sa_column=Column(Text))
    subtotal: float = 0
    discount: float = 0
    tax: float = 0
    total: float = 0
    status: QuoteStatus = QuoteStatus.draft
    notes: str | None = Field(default=None, sa_column=Column(Text))
    terms: str | None = Field(default="Valid for 14 days. Payment due upon completion.", sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    customer: Customer | None = Relationship(back_populates="quotes")
    job: Job | None = Relationship(back_populates="quotes")
    invoices: list["Invoice"] = Relationship(back_populates="quote")


class Invoice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    invoice_number: str
    customer_id: int | None = Field(default=None, foreign_key="customer.id")
    job_id: int | None = Field(default=None, foreign_key="job.id")
    quote_id: int | None = Field(default=None, foreign_key="quote.id")
    line_items: str = Field(default="[]", sa_column=Column(Text))
    subtotal: float = 0
    tax: float = 0
    total: float = 0
    amount_paid: float = 0
    due_date: date | None = None
    status: InvoiceStatus = InvoiceStatus.draft
    created_at: datetime = Field(default_factory=datetime.utcnow)

    customer: Customer | None = Relationship(back_populates="invoices")
    job: Job | None = Relationship(back_populates="invoices")
    quote: Quote | None = Relationship(back_populates="invoices")

    @property
    def balance_due(self) -> float:
        return max(self.total - self.amount_paid, 0)


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None, sa_column=Column(Text))
    customer_id: int | None = Field(default=None, foreign_key="customer.id")
    job_id: int | None = Field(default=None, foreign_key="job.id")
    due_date: date | None = None
    priority: Priority = Priority.medium
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    customer: Customer | None = Relationship(back_populates="tasks")
    job: Job | None = Relationship(back_populates="tasks")


class BusinessSettings(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    business_name: str = "ServicePilot Demo Co."
    owner_name: str = "BeauDevCode"
    email: str = "owner@example.com"
    phone: str = "(555) 123-4567"
    default_tax_rate: float = 8.25
    default_service_area: str = "Local service area"
    preferred_currency: str = "USD"

