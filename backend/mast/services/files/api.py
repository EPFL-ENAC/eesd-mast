"""
Handle / uploads
"""
from mast.config import settings
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from mast.services.files.s3client import S3_SERVICE

from fastapi import Depends, Security, APIRouter

from mast.services.files.size import size_checker
from mast.auth import get_api_key

from pydantic import BaseModel


class FilePath(BaseModel):
    paths: list[str]


router = APIRouter()

# Object of S3_SERVICE Class
s3_client = S3_SERVICE(settings.S3_ENDPOINT_PROTOCOL + settings.S3_ENDPOINT_HOSTNAME,
                       settings.S3_ACCESS_KEY_ID,
                       settings.S3_SECRET_ACCESS_KEY, settings.S3_REGION)

@router.post("/files",
             status_code=200,
             description="-- Upload jpg/png/pdf or any assets to S3 --",
             dependencies=[Depends(size_checker)])
async def PostUpload(
        files: list[UploadFile] = File(description="multiple file upload"), api_key: str = Security(get_api_key)):
    return {"filenames": [await s3_client.upload_file(file) for file in files]}

@router.delete("/files",
               status_code=204,
               description="-- Delete assest present in S3 --",
               )
async def DeleteUpload(filePath: FilePath, api_key: str = Security(get_api_key)):
    [await s3_client.delete_file(path) for path in filePath.paths]
    return
