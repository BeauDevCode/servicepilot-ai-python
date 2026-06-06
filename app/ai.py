from __future__ import annotations

import json
import re

from openai import OpenAI

from app.config import get_settings
from app.schemas import ExtractedRequest

SERVICE_KEYWORDS = {
    "brake|honda|toyota|car|vehicle|engine|oil|tire": "Mobile Mechanic",
    "clean|apartment|house|deep clean|pets": "Cleaning",
    "yard|lawn|landscape|grass|mulch": "Landscaping",
    "photo|shoot|wedding|portrait": "Photography",
    "hair|cut|barber|fade": "Barber",
    "tutor|math|homework|lesson": "Tutoring",
    "pressure|wash|driveway|siding": "Pressure Washing",
    "repair|fix|install|leak|drywall": "Home Repair",
}


def _detect_service(message: str) -> str:
    lower = message.lower()
    for pattern, service in SERVICE_KEYWORDS.items():
        if re.search(pattern, lower):
            return service
    return "General Service"


def mock_extract_request(message: str) -> ExtractedRequest:
    service = _detect_service(message)
    lower = message.lower()
    preferred = None
    for token in ["today", "tomorrow", "friday", "saturday", "sunday", "morning", "afternoon", "evening"]:
        if token in lower:
            preferred = token.title() if preferred is None else f"{preferred}, {token.title()}"

    phone_match = re.search(r"(\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})", message)
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", message)
    name_match = re.search(r"(?:my name is|i'?m|this is)\s+([A-Z][a-z]+)", message, re.I)
    bedrooms = re.search(r"(\d+)\s*(?:bed|bedroom|br)", lower)
    vehicle = re.search(r"((?:19|20)\d{2}\s+[a-z]+(?:\s+(?!and\b|it\b|with\b|that\b|making\b)[a-z0-9-]+){0,2})", lower)

    if service == "Mobile Mechanic":
        title = "Brake or vehicle repair request" if "brake" in lower else "Mobile mechanic request"
        low, high = 120, 420
        checklist = ["Confirm vehicle year/make/model", "Ask if vehicle is safe to drive", "Inspect issue onsite", "Price parts and labor", "Send approval before repair"]
    elif service == "Cleaning":
        title = "Residential deep cleaning request"
        low, high = 150, 350
        checklist = ["Confirm bedroom and bathroom count", "Ask about pets and supplies", "Confirm access instructions", "Estimate deep clean duration", "Send quote and arrival window"]
    elif service == "Landscaping":
        title = "Yard service request"
        low, high = 80, 300
        checklist = ["Confirm property size", "Ask for photos", "Check disposal needs", "Confirm schedule", "Prepare equipment list"]
    else:
        title = f"{service} request"
        low, high = 75, 250
        checklist = ["Confirm scope", "Ask for location", "Request photos if helpful", "Confirm deadline", "Send quote draft"]

    details = vehicle.group(1).title() if vehicle else bedrooms.group(0) if bedrooms else None
    missing = []
    if not phone_match and not email_match:
        missing.append("Best contact phone or email")
    if not preferred:
        missing.append("Preferred date and time")
    if "address" not in lower and " at " not in lower:
        missing.append("Service address or neighborhood")

    return ExtractedRequest(
        customer_name=name_match.group(1).title() if name_match else "New Lead",
        phone=phone_match.group(1) if phone_match else None,
        email=email_match.group(0) if email_match else None,
        service_category=service,
        job_title=title,
        job_description=message.strip(),
        details=details,
        urgency="High" if any(word in lower for word in ["asap", "urgent", "today", "emergency"]) else "Normal",
        preferred_date_time=preferred,
        missing_information=missing,
        suggested_quote_low=low,
        suggested_quote_high=high,
        suggested_checklist=checklist,
        follow_up_message=(
            "Thanks for reaching out. I can help with this. "
            f"To give you an accurate quote for the {service.lower()} job, can you send "
            f"{', '.join(missing) if missing else 'any extra details or photos'}?"
        ),
    )


async def extract_request(message: str) -> ExtractedRequest:
    settings = get_settings()
    if not settings.openai_api_key:
        return mock_extract_request(message)

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = (
        "Extract a service-business intake request as JSON matching these keys: "
        "customer_name, phone, email, service_category, job_title, job_description, details, urgency, "
        "preferred_date_time, location, missing_information, suggested_quote_low, suggested_quote_high, "
        "suggested_checklist, follow_up_message. Be conservative and practical.\n\n"
        f"Customer message: {message}"
    )
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "system", "content": "You turn messy customer messages into structured job intake data."}, {"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    content = response.choices[0].message.content or "{}"
    try:
        return ExtractedRequest.model_validate(json.loads(content))
    except Exception:
        return mock_extract_request(message)
