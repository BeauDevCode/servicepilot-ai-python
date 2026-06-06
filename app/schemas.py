from datetime import date, datetime

from pydantic import BaseModel, Field


class ExtractedRequest(BaseModel):
    customer_name: str | None = None
    phone: str | None = None
    email: str | None = None
    service_category: str
    job_title: str
    job_description: str
    details: str | None = None
    urgency: str = "Normal"
    preferred_date_time: str | None = None
    location: str | None = None
    missing_information: list[str] = Field(default_factory=list)
    suggested_quote_low: float = 0
    suggested_quote_high: float = 0
    suggested_checklist: list[str] = Field(default_factory=list)
    follow_up_message: str


class DashboardStats(BaseModel):
    total_customers: int
    open_jobs: int
    pending_quotes: int
    unpaid_invoices: int
    completed_jobs: int
    estimated_monthly_revenue: float
    overdue_followups: int
    tasks_due_today: int


class LineItem(BaseModel):
    description: str
    quantity: float = 1
    unit_price: float = 0

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


class TimelineEvent(BaseModel):
    label: str
    when: datetime | date | None = None
    detail: str | None = None

