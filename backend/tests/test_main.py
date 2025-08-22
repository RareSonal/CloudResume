import os
import cgi  # For parsing headers
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_azure_clients():
    with patch("api.main.TableServiceClient") as mock_table_service_client, \
         patch("api.main.BlobServiceClient") as mock_blob_service_client:

        # Mock table client and its methods
        mock_table_client_instance = MagicMock()
        mock_table_service_client.from_connection_string.return_value.get_table_client.return_value = mock_table_client_instance

        # Simulate get_entity raising ResourceNotFoundError once, then returning an entity
        def get_entity_side_effect(partition_key, row_key):
            if not hasattr(get_entity_side_effect, "called"):
                get_entity_side_effect.called = True
                # Simulate ResourceNotFoundError on first call
                from azure.core.exceptions import ResourceNotFoundError
                raise ResourceNotFoundError("Entity not found")
            return {"PartitionKey": partition_key, "RowKey": row_key, "count": 2}

        mock_table_client_instance.get_entity.side_effect = get_entity_side_effect
        mock_table_client_instance.create_entity.return_value = None
        mock_table_client_instance.update_entity.return_value = None

        # Mock blob client and its methods
        mock_blob_client_instance = MagicMock()
        mock_blob_service_client.from_connection_string.return_value.get_container_client.return_value.get_blob_client.return_value = mock_blob_client_instance
        mock_blob_client_instance.download_blob.return_value.readall.return_value = b"%PDF-1.4 mock pdf content"

        yield  # Run the tests with mocks active

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
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")
