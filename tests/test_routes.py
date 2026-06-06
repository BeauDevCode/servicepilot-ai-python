from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_and_core_pages_render():
    with TestClient(app) as client:
        for path in ["/dashboard", "/ai-assistant", "/customers", "/jobs", "/quotes", "/invoices", "/tasks", "/analytics", "/settings"]:
            response = client.get(path)
            assert response.status_code == 200, path
            assert "ServicePilot AI" in response.text


def test_ai_intake_post_renders_extraction():
    with TestClient(app) as client:
        response = client.post("/ai-assistant", data={"message": "can you clean my 2 bedroom apartment friday afternoon with pets"})
        assert response.status_code == 200
        assert "Cleaning" in response.text
        assert "Quote Range" in response.text
