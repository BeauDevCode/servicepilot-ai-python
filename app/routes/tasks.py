from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.models import Customer, Job, Priority
from app.services.task_service import complete_task, create_task, list_tasks
from app.templating import templates

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def tasks_page(request: Request, completed: bool | None = None, session: Session = Depends(get_session)):
    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "active": "tasks",
            "tasks": list_tasks(session, completed),
            "customers": list(session.exec(select(Customer))),
            "jobs": list(session.exec(select(Job))),
            "priorities": Priority,
            "completed": completed,
        },
    )


@router.post("")
def add_task(title: str = Form(...), description: str | None = Form(None), customer_id: int | None = Form(None), job_id: int | None = Form(None), due_date_value: str | None = Form(None), priority: Priority = Form(Priority.medium), session: Session = Depends(get_session)):
    due = date.fromisoformat(due_date_value) if due_date_value else None
    create_task(session, title=title, description=description, customer_id=customer_id, job_id=job_id, due_date=due, priority=priority)
    return RedirectResponse("/tasks", status_code=303)


@router.post("/{task_id}/complete")
def complete(task_id: int, session: Session = Depends(get_session)):
    complete_task(session, task_id)
    return RedirectResponse("/tasks", status_code=303)
