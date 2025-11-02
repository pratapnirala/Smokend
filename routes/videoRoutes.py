from fastapi import APIRouter, HTTPException
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from config.config import config
from azure.storage.blob import BlobServiceClient

videoRouter = APIRouter()
# ===== Helper Functions =====

# === Create Blob Service Client ===
try:
    blob_service_client = BlobServiceClient(
        account_url=f"https://{config.account_name}.blob.core.windows.net",
        credential=config.account_key
    )

except Exception as e:
    raise HTTPException(status_code=500, detail=f"Blob connection failed: {str(e)}")


@videoRouter.get("/generate-sas")
async def generate_sas_for_all_files():
    try:
        container_name = config.container_name

        # Get container client
        container_client = blob_service_client.get_container_client(container_name)

        # List all blobs
        blob_list = container_client.list_blobs()

        sas_urls = []
        for blob in blob_list:
            sas_token = generate_blob_sas(
                account_name=blob_service_client.account_name,
                container_name=container_name,
                blob_name=blob.name,
                account_key=config.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(days=7),
            )
            secure_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob.name}?{sas_token}"
            sas_urls.append({"file_name": blob.name, "url": secure_url})

        return {"count": len(sas_urls), "sas_urls": sas_urls}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))