

from fastapi import FastAPI, HTTPException, UploadFile, File
from imghst.app.configuration.configuration import Configuration
from loguru import logger
import aiofiles
from datetime import datetime

import filetype

from .request_models import (
    HealthCheckRequest,
    NewImageRequestResponse
)

app = FastAPI()


@app.get("/health", response_model=HealthCheckRequest)
async def health_check() -> HealthCheckRequest:
    return HealthCheckRequest(
        systemStatus=True
    )


@app.post("/uploadImage/{apiKey}", response_model=NewImageRequestResponse)
async def upload_image_to_file_path(apiKey, image_upload: UploadFile = File(...)) -> NewImageRequestResponse:
    
    if apiKey != Configuration.api_request_key:
        raise HTTPException(status_code=400, detail="Invalid API Key.")

    current_configuration_image_path = Configuration.image_hosting_folder
    
    if not current_configuration_image_path.exists():
        raise HTTPException(status_code=500, detail="Improper configuration was set. The current configuration image hosting folder does not exist.")
    

    _supported_file_types = [
        "image/jpeg",
        "image/jpx",
        "image/png",
        "image/gif",
        "image/webp",
        "image/x-canon-cr2",
        "image/tiff",
        "image/bmp",
        "image/vnd.ms-photo",
        "image/vnd.adobe.photoshop",
        "image/x-icon",
        "image/heic"
    ]

    if image_upload.content_type not in _supported_file_types:
        await image_upload.file.close()
        raise HTTPException(status_code=400, detail="Unsupported file type uploaded.")
    
    
    # check if valid.
    try:
        detect_file_type = filetype.guess(await image_upload.read())
        if detect_file_type is None:
            raise HTTPException(status_code=400, detail="Unknown file type was uploaded.")

        if detect_file_type.mime != image_upload.content_type:
            raise HTTPException(status_code=500, detail="Mismatch content type header and mime value of object.")
    except Exception:
        logger.exception("Unknown error occurred for detecting file type.")
        raise HTTPException(status_code=500, detail="System error on detecting file type.")

    generate_a_unique_id = Configuration.image_unique_file_name()
    
    async with aiofiles.open(str(current_configuration_image_path / f"{generate_a_unique_id}.{detect_file_type.extension}"), "wb") as opened_file:
        await image_upload.seek(0)
        await opened_file.write(await image_upload.read())
        image_upload.file.close()

    return NewImageRequestResponse(
        api_status=True,
        date_processed=datetime.now().isoformat(),
        file_direct_path_name=str(current_configuration_image_path / f"{generate_a_unique_id}.{detect_file_type.extension}")
    )