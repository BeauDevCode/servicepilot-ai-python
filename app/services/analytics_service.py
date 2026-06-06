from datetime import date

from sqlmodel import Session, func, select

from app.models import Customer, Invoice, InvoiceStatus, Job, JobStatus, Quote, QuoteStatus, Task
from app.schemas import DashboardStats


def dashboard_stats(session: Session) -> DashboardStats:
    total_customers = session.exec(select(func.count(Customer.id))).one()
    open_jobs = session.exec(select(func.count(Job.id)).where(Job.status != JobStatus.completed, Job.status != JobStatus.cancelled)).one()
    pending_quotes = session.exec(select(func.count(Quote.id)).where(Quote.status.in_([QuoteStatus.draft, QuoteStatus.sent]))).one()
    unpaid_invoices = session.exec(select(func.count(Invoice.id)).where(Invoice.status.in_([InvoiceStatus.sent, InvoiceStatus.overdue]))).one()
    completed_jobs = session.exec(select(func.count(Job.id)).where(Job.status == JobStatus.completed)).one()
    revenue = session.exec(select(func.coalesce(func.sum(Invoice.total), 0)).where(Invoice.status == InvoiceStatus.paid)).one()
    overdue = session.exec(select(func.count(Task.id)).where(Task.due_date < date.today(), Task.completed == False)).one()  # noqa: E712
    due_today = session.exec(select(func.count(Task.id)).where(Task.due_date == date.today(), Task.completed == False)).one()  # noqa: E712
    return DashboardStats(
        total_customers=total_customers,
        open_jobs=open_jobs,
        pending_quotes=pending_quotes,
        unpaid_invoices=unpaid_invoices,
        completed_jobs=completed_jobs,
        estimated_monthly_revenue=revenue,
        overdue_followups=overdue,
        tasks_due_today=due_today,
    )


def analytics_summary(session: Session) -> dict[str, object]:
    invoices = list(session.exec(select(Invoice)))
    jobs = list(session.exec(select(Job)))
    quotes = list(session.exec(select(Quote)))
    revenue_by_service: dict[str, float] = {}
    for job in jobs:
        revenue_by_service[job.service_type] = revenue_by_service.get(job.service_type, 0) + float(job.final_price or job.estimated_price or 0)

    accepted = len([quote for quote in quotes if quote.status == QuoteStatus.accepted])
    rate = round((accepted / len(quotes)) * 100, 1) if quotes else 0
    paid = [invoice for invoice in invoices if invoice.status == InvoiceStatus.paid]
    avg_job_value = round(sum(invoice.total for invoice in paid) / len(paid), 2) if paid else 0
    return {
        "revenue_this_month": sum(invoice.total for invoice in paid),
        "revenue_by_service": revenue_by_service,
        "open_invoices": len([invoice for invoice in invoices if invoice.status in {InvoiceStatus.sent, InvoiceStatus.overdue}]),
        "paid_invoices": len(paid),
        "quote_acceptance_rate": rate,
        "average_job_value": avg_job_value,
        "jobs_completed": len([job for job in jobs if job.status == JobStatus.completed]),
        "tasks_completed": session.exec(select(func.count(Task.id)).where(Task.completed == True)).one(),  # noqa: E712
        "customers_added": session.exec(select(func.count(Customer.id))).one(),
        "followups_overdue": session.exec(select(func.count(Task.id)).where(Task.due_date < date.today(), Task.completed == False)).one(),  # noqa: E712
    }

