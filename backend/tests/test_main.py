import os
import cgi  # For parsing headers
from fastapi.testclient import TestClient
from api.main import app  # Adjusted import path to avoid "module not found"

client = TestClient(app)

def test_visitor_counter():
    response = client.get("/api/visitor")
    assert response.status_code == 200

    data = response.json()
    assert "count" in data
    assert isinstance(data["count"], int)

def test_resume_download():
    response = client.get("/api/resume")
    assert response.status_code == 200

    expected_filename = os.getenv("BLOB_NAME", "SonaliMandrupkar_CloudResume.pdf")

    content_disposition = response.headers.get("Content-Disposition")
    value, params = cgi.parse_header(content_disposition)

    assert value == "attachment"
    assert params.get("filename") == expected_filename
