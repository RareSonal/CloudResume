import os
import io
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient, UpdateMode
from azure.core.exceptions import ResourceNotFoundError
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Enable CORS (for local development, allows all origins — update for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://127.0.0.1:5500"] or your frontend domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")
BLOB_NAME = os.getenv("BLOB_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")
PARTITION_KEY = "resume"
ROW_KEY = "visitor"

@app.get("/api/visitor")
async def get_visitor_count():
    table_client = TableServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    ).get_table_client(TABLE_NAME)

    try:
        entity = table_client.get_entity(partition_key=PARTITION_KEY, row_key=ROW_KEY)
        entity["count"] += 1
        table_client.update_entity(entity, mode=UpdateMode.REPLACE)
    except ResourceNotFoundError:
        entity = {"PartitionKey": PARTITION_KEY, "RowKey": ROW_KEY, "count": 1}
        table_client.create_entity(entity)

    return JSONResponse(content={"count": entity["count"]})

@app.get("/api/resume")
async def download_resume():
    blob_service_client = BlobServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    )
    blob_client = blob_service_client.get_container_client(BLOB_CONTAINER).get_blob_client(BLOB_NAME)

    stream = io.BytesIO()
    download_stream = blob_client.download_blob()
    stream.write(download_stream.readall())
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment;filename={BLOB_NAME}"},
    )
