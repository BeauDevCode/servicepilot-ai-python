from fastapi import APIRouter, Request

from app.templating import templates

router = APIRouter()


@router.get("/")
def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request, "active": "landing"})
