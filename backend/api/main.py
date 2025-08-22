import os
import io
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient, UpdateMode
from azure.core.exceptions import ResourceNotFoundError

# === Create FastAPI app ===
app = FastAPI()

# === Configure CORS for Production ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://raresonalcloudresume.z30.web.core.windows.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Constants for table entity ===
PARTITION_KEY = "resume"
ROW_KEY = "visitor"

# === Helper: Fetch and validate env vars only when needed ===
def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value

# === API endpoint: Visitor Counter ===
@app.get("/api/visitor")
async def get_visitor_count():
    conn_str = get_env_var("AZURE_STORAGE_CONNECTION_STRING")
    table_name = get_env_var("TABLE_NAME")

    table_client = TableServiceClient.from_connection_string(conn_str).get_table_client(table_name)

    try:
        entity = table_client.get_entity(partition_key=PARTITION_KEY, row_key=ROW_KEY)
        entity["count"] += 1
        table_client.update_entity(entity, mode=UpdateMode.REPLACE)
    except ResourceNotFoundError:
        entity = {"PartitionKey": PARTITION_KEY, "RowKey": ROW_KEY, "count": 1}
        table_client.create_entity(entity)

    return JSONResponse(content={"count": entity["count"]})

# === API endpoint: Resume Download ===
@app.get("/api/resume")
async def download_resume():
    conn_str = get_env_var("AZURE_STORAGE_CONNECTION_STRING")
    container = get_env_var("BLOB_CONTAINER")
    blob_name = get_env_var("BLOB_NAME")

    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_client = blob_service_client.get_container_client(container).get_blob_client(blob_name)

    stream = io.BytesIO()
    download_stream = blob_client.download_blob()
    stream.write(download_stream.readall())
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={blob_name}"},
    )
