from aiobotocore.session import get_session
from io import BytesIO
from fastapi.logger import logger
from typing import Tuple
import datetime
from PIL import Image
from fastapi.exceptions import HTTPException
from app.config import config
from app.utils.mimetype import image_mimetypes, pdf_mimetypes
from fastapi.datastructures import UploadFile
import os
import urllib.parse

class S3_SERVICE(object):

    def __init__(self, s3_endpoint_url, s3_access_key_id, s3_secret_access_key, region, *args,
                 **kwargs):
        self.s3_endpoint_url = s3_endpoint_url
        self.s3_access_key_id = s3_access_key_id
        self.s3_secret_access_key = s3_secret_access_key
        self.region = region
        self.with_webp = False

    async def get_file(self, file_path: str):
        # get file from file path
        if file_path.startswith(config.S3_PATH_PREFIX):
            session = get_session()
            async with session.create_client(
                    's3',
                    region_name=self.region,
                    endpoint_url=self.s3_endpoint_url,
                    aws_secret_access_key=self.s3_secret_access_key,
                    aws_access_key_id=self.s3_access_key_id) as client:
                try:
                    response = await client.get_object(
                        Bucket=config.S3_BUCKET, Key=file_path)
                    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        # Read the content of the S3 object
                        file_content = await response['Body'].read()
                        return file_content, response["ContentType"]
                except Exception as e:
                    return False, False
        return False, False

    async def upload_file(self, upload_file: UploadFile):
        # if mimetype is image upload image
        if upload_file.content_type in image_mimetypes:
            return await self._upload_image(upload_file)
        elif upload_file.content_type in pdf_mimetypes:
            return await self._upload_with_type(upload_file, "Report")
        return await self._upload_with_type(upload_file, "Other")

    async def delete_file(self, file_path: str):
        if file_path.startswith(config.S3_PATH_PREFIX):
            # delete file_path
            session = get_session()
            async with session.create_client(
                    's3',
                    region_name=self.region,
                    endpoint_url=self.s3_endpoint_url,
                    aws_secret_access_key=self.s3_secret_access_key,
                    aws_access_key_id=self.s3_access_key_id) as client:
                response = await client.delete_object(
                    Bucket=config.S3_BUCKET, Key=file_path)
                if response["ResponseMetadata"]["HTTPStatusCode"] == 204:
                    logger.info(
                        f"File deleted path : {self.s3_endpoint_url}/{config.S3_BUCKET}/{file_path}")
                    return file_path
        return False

    #
    # Private methods
    #

    async def _convert_image(self, upload_file: UploadFile):
        request_object_content = await upload_file.read()
        origin_BytesIo = BytesIO(request_object_content)
        image = Image.open(origin_BytesIo)
        data = BytesIO()
        image.save(data, format="webp", quality=60)
        return (data, origin_BytesIo)

    async def _get_unique_filename(self,
                                  filename: str,
                                  ext: str = "") -> Tuple[str, str]:
        current_time = datetime.datetime.now()
        # generate unique name for the file
        unique_name = str(current_time.timestamp()).replace('.', '')
        split_file_name = os.path.splitext(filename)
        ext = ext if ext != "" else split_file_name[1]
        name = split_file_name[0]
        uri_component_encoded = split_file_name[0]
        return (f"{unique_name}{uri_component_encoded}{ext}", name)

    async def _upload_image(self, upload_file: UploadFile):
        # convert to bytes
        (data, origin_data) = await self._convert_image(upload_file)

        # Webp converted image
        if self.with_webp:
            mimetype = "image/webp"
            (unique_name,
            name) = await self._get_unique_filename(upload_file.filename, ".webp")

            key = f"{config.S3_PATH_PREFIX}{unique_name}"
            uploads3 = await self._upload_fileobj(bucket=config.S3_BUCKET,
                                                key=key,
                                                data=data.getvalue(),
                                                mimetype=mimetype)
            
            if not uploads3:
                raise HTTPException(status_code=500,
                                detail="Failed to upload image to S3")
        
        # Original image
        (unique_origin_name,
         origin_name) = await self._get_unique_filename(upload_file.filename)
        key_origin = f"{config.S3_PATH_PREFIX}{unique_origin_name}"
        uploads3Origin = await self._upload_fileobj(
            bucket=config.S3_BUCKET,
            key=key_origin,
            data=origin_data.getvalue(),
            mimetype=upload_file.content_type)
        
        if not uploads3Origin:
            raise HTTPException(status_code=500,
                                    detail="Failed to upload image to S3")

        if self.with_webp:
            # response http to be used by the frontend
            return {
                "path": urllib.parse.quote(key),
                "origin_path": urllib.parse.quote(key_origin),
                "name": name,
                "type": "Image"
            }
        else:
            # response http to be used by the frontend
            return {
                "path": urllib.parse.quote(key_origin),
                "name": origin_name,
                "type": "Image"
            }

    async def _upload_with_type(self,
                               upload_file: UploadFile,
                               type: str = "Other"):
        # only four types allowed: Image / Drawing / Report / Other
        (filename, name) = await self._get_unique_filename(upload_file.filename)
        key = f"{config.S3_PATH_PREFIX}{filename}"
        uploads3 = await self._upload_fileobj(bucket=config.S3_BUCKET,
                                             key=key,
                                             data=upload_file.file._file,
                                             mimetype=upload_file.content_type)
        if uploads3:
            # response http to be used by the frontend
            return {"path": urllib.parse.quote(key), "name": name, "type": type}
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to upload file to S3 EPFL server")

    async def _upload_fileobj(self, data: BytesIO, bucket: str, key: str,
                             mimetype: str):
        session = get_session()
        async with session.create_client(
                's3',
                region_name=self.region,
                endpoint_url=self.s3_endpoint_url,
                aws_secret_access_key=self.s3_secret_access_key,
                aws_access_key_id=self.s3_access_key_id) as client:
            file_upload_response = await client.put_object(
                Bucket=bucket,
                Key=key,
                Body=data,
                ACL="public-read",
                ContentType=mimetype)

            if file_upload_response["ResponseMetadata"][
                    "HTTPStatusCode"] == 200:
                logger.info(
                    f"File uploaded path : {self.s3_endpoint_url}/{bucket}/{key}")
                return True
        return False
    

s3_client = S3_SERVICE(config.S3_ENDPOINT_PROTOCOL + config.S3_ENDPOINT_HOSTNAME,
                       config.S3_ACCESS_KEY_ID,
                       config.S3_SECRET_ACCESS_KEY, config.S3_REGION)