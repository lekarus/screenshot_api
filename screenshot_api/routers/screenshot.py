import os
from typing import Annotated
import uuid

import boto3
from boto3.exceptions import S3UploadFailedError
from fastapi import APIRouter, Depends, UploadFile, HTTPException

from config import settings
from models import User
from utils.auth import get_current_user

screenshot_router = APIRouter()


@screenshot_router.post("/upload_file")
async def upload_file(current_user: Annotated[User, Depends(get_current_user)], file: UploadFile):
    """
    method to store file locally, then upload to s3 bucket
    """
    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="file must be an image")
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(settings.bucket_name)

    with open("/tmp/" + file.filename, "wb") as local_file:
        local_file.write(await file.read())

    try:
        bucket.upload_file(
            "/tmp/" + file.filename,
            current_user.id + "/" + f"{str(uuid.uuid4())}.{file.filename.rsplit('.')[-1]}"
        )
    except S3UploadFailedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        os.remove("/tmp/" + file.filename)

    return {
        "msg": f"{file.filename} successfully uploaded"
    }
