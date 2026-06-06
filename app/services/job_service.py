from datetime import datetime

from sqlmodel import Session, col, select

from app.models import Job


def list_jobs(session: Session, q: str | None = None, status: str | None = None, service_type: str | None = None) -> list[Job]:
    statement = select(Job).order_by(col(Job.created_at).desc())
    if q:
        statement = statement.where(Job.title.contains(q) | Job.description.contains(q))
    if status:
        statement = statement.where(Job.status == status)
    if service_type:
        statement = statement.where(Job.service_type == service_type)
    return list(session.exec(statement))


def get_job(session: Session, job_id: int) -> Job | None:
    return session.get(Job, job_id)


def create_job(session: Session, **data: object) -> Job:
    job = Job(**data)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def update_job(session: Session, job: Job, **data: object) -> Job:
    for key, value in data.items():
        setattr(job, key, value)
    job.updated_at = datetime.utcnow()
    session.add(job)
    session.commit()
    session.refresh(job)
    return job

