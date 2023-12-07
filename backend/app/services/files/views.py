"""
Handle / uploads
"""
from app.config import config
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from app.services.files.s3client import S3_SERVICE

from fastapi import Depends, Security, APIRouter, HTTPException
from fastapi.responses import StreamingResponse, Response

from app.utils.mimetype import image_mimetypes
from app.services.files.size import size_checker
from app.auth import get_api_key

from pydantic import BaseModel


class FilePath(BaseModel):
    paths: list[str]


router = APIRouter()

s3_client = S3_SERVICE(config.S3_ENDPOINT_PROTOCOL + config.S3_ENDPOINT_HOSTNAME,
                       config.S3_ACCESS_KEY_ID,
                       config.S3_SECRET_ACCESS_KEY, config.S3_REGION)

@router.get("/{file_path:path}",
             status_code=200,
             description="-- Download jpg/png/pdf or any assets from S3 --")
async def get_file(file_path: str):
    (body, content_type) = await s3_client.get_file(file_path)
    if body:
      if content_type in image_mimetypes:
        # inline image
        return Response(content=body)
      else:
        # download file 
        return Response(content=body, media_type=content_type)
    else:
      raise HTTPException(status_code=404, detail="File not found")

@router.post("",
             status_code=200,
             description="-- Upload jpg/png/pdf or any assets to S3 --",
             dependencies=[Depends(size_checker)])
async def upload_files(
        files: list[UploadFile] = File(description="multiple file upload"), api_key: str = Security(get_api_key)):
    return {"files": [await s3_client.upload_file(file) for file in files]}


@router.delete("",
               status_code=204,
               description="-- Delete asset present in S3 --",
               )
async def delete_files(filePath: FilePath, api_key: str = Security(get_api_key)):
    [await s3_client.delete_file(path) for path in filePath.paths]
    return