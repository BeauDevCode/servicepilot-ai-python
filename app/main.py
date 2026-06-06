from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR, get_settings
from app.database import init_db
from app.routes import ai_assistant, analytics, api, customers, dashboard, invoices, jobs, landing, quotes, settings, tasks
from app.seed_data import seed_demo_data

settings_obj = get_settings()
app = FastAPI(title=settings_obj.app_name, description=settings_obj.app_tagline, version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    if settings_obj.demo_mode:
        seed_demo_data()


@app.middleware("http")
async def add_template_context(request: Request, call_next):
    request.state.settings = settings_obj
    return await call_next(request)


for router in [
    landing.router,
    dashboard.router,
    ai_assistant.router,
    customers.router,
    jobs.router,
    quotes.router,
    invoices.router,
    tasks.router,
    analytics.router,
    settings.router,
    api.router,
]:
    app.include_router(router)
