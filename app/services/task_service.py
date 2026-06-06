from datetime import date

from sqlmodel import Session, col, select

from app.models import Task


def list_tasks(session: Session, completed: bool | None = None) -> list[Task]:
    statement = select(Task).order_by(col(Task.due_date), col(Task.created_at).desc())
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    return list(session.exec(statement))


def create_task(session: Session, **data: object) -> Task:
    task = Task(**data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def complete_task(session: Session, task_id: int) -> Task | None:
    task = session.get(Task, task_id)
    if not task:
        return None
    task.completed = True
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def due_today_count(session: Session) -> int:
    return len(list(session.exec(select(Task).where(Task.due_date == date.today(), Task.completed == False))))  # noqa: E712

