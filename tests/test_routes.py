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


def test_full_ai_workflow_creates_records_and_pages_update():
    message = "hey bro can you come saturday to fix my brakes i got a 2008 honda accord and it making grinding sound how much"
    with TestClient(app) as client:
        create_response = client.post("/ai-assistant/create-workflow", data={"message": message}, follow_redirects=False)
        assert create_response.status_code == 303
        assert create_response.headers["location"].startswith("/jobs/")

        job_detail = client.get(create_response.headers["location"])
        assert job_detail.status_code == 200
        assert "Mobile Mechanic" in job_detail.text
        assert "Brake" in job_detail.text or "brake" in job_detail.text

        for path, expected in [
            ("/dashboard", "Open Jobs"),
            ("/customers", "New Lead"),
            ("/jobs", "Brake"),
            ("/quotes", "AI-assisted draft"),
            ("/tasks", "Follow up with New Lead"),
            ("/analytics", "Revenue By Service Type"),
        ]:
            response = client.get(path)
            assert response.status_code == 200, path
            assert expected in response.text


def test_manual_forms_accept_blank_optional_relationships():
    with TestClient(app) as client:
        quote_response = client.post("/quotes", data={"customer_id": "", "job_id": "", "description": "Diagnostic", "amount": "95"}, follow_redirects=False)
        invoice_response = client.post(
            "/invoices",
            data={"customer_id": "", "job_id": "", "description": "Service call", "amount": "125"},
            follow_redirects=False,
        )
        task_response = client.post(
            "/tasks",
            data={"customer_id": "", "job_id": "", "title": "Call customer", "description": "Confirm appointment", "priority": "Medium"},
            follow_redirects=False,
        )
        assert quote_response.status_code == 303
        assert invoice_response.status_code == 303
        assert task_response.status_code == 303


def test_settings_update_route():
    with TestClient(app) as client:
        response = client.post(
            "/settings",
            data={
                "business_name": "QA Service Co.",
                "owner_name": "QA Owner",
                "email": "qa@example.com",
                "phone": "(555) 000-1111",
                "default_tax_rate": "7.5",
                "default_service_area": "Chicago",
                "preferred_currency": "USD",
            },
            follow_redirects=False,
        )
        assert response.status_code == 303
        settings_page = client.get("/settings")
        assert "QA Service Co." in settings_page.text
