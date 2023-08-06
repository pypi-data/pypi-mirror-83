
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic.class_validators import validator

from .configuration.configuration import Configuration


class NewImageRequestResponse(BaseModel):
    """ Response model after uploading a new image """

    api_status: bool
    date_processed: datetime
    file_direct_path_name: str

    
class HealthCheckRequest(BaseModel):
    """ Request model for health check endpoint """
    
    systemStatus: bool

