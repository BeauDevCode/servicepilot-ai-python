from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.config import get_settings
from app.database import get_session
from app.models import BusinessSettings
from app.templating import templates

router = APIRouter(prefix="/settings", tags=["settings"])


def get_business_settings(session: Session) -> BusinessSettings:
    found = session.exec(select(BusinessSettings)).first()
    if found:
        return found
    settings = BusinessSettings()
    session.add(settings)
    session.commit()
    session.refresh(settings)
    return settings


@router.get("")
def settings_page(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("settings.html", {"request": request, "active": "settings", "business": get_business_settings(session), "app_settings": get_settings()})


@router.post("")
def update_settings(
    business_name: str = Form(...),
    owner_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    default_tax_rate: float = Form(...),
    default_service_area: str = Form(...),
    preferred_currency: str = Form(...),
    session: Session = Depends(get_session),
):
    business = get_business_settings(session)
    business.business_name = business_name
    business.owner_name = owner_name
    business.email = email
    business.phone = phone
    business.default_tax_rate = default_tax_rate
    business.default_service_area = default_service_area
    business.preferred_currency = preferred_currency
    session.add(business)
    session.commit()
    return RedirectResponse("/settings", status_code=303)
