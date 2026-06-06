from app.ai import mock_extract_request


def test_mock_ai_extracts_mechanic_request():
    result = mock_extract_request("hey can you come saturday to fix my brakes i got a 2008 honda accord and grinding sound")
    assert result.service_category == "Mobile Mechanic"
    assert "brake" in result.job_title.lower() or "vehicle" in result.job_title.lower()
    assert result.suggested_quote_high > result.suggested_quote_low
    assert result.suggested_checklist


def test_mock_ai_extracts_cleaning_request():
    result = mock_extract_request("deep clean my 2 bedroom apartment friday afternoon with pets")
    assert result.service_category == "Cleaning"
    assert "Best contact" in result.missing_information[0]

