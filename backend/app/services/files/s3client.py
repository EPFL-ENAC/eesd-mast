from aiobotocore.session import get_session
from io import BytesIO
from fastapi.logger import logger
from fastapi.exceptions import HTTPException
from typing import Tuple
from PIL import Image
from app.config import config
from app.utils.mimetype import image_mimetypes, model_mimetypes
from fastapi.datastructures import UploadFile
import os
import urllib.parse
import mimetypes


class S3_SERVICE(object):

    def __init__(self, s3_endpoint_url, s3_access_key_id, s3_secret_access_key, region, *args,
                 **kwargs):
        self.s3_endpoint_url = s3_endpoint_url
        self.s3_access_key_id = s3_access_key_id
        self.s3_secret_access_key = s3_secret_access_key
        self.region = region

    async def get_file(self, file_path: str):
        """Extract file content and mimetype from S3 storage

        Args:
            file_path (str): Path of the file in S3

        Returns:
            Tuple: File content and mimetype
        """
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

    async def upload_local_file(self, parent_path, file_path: str, s3_folder: str = ""):
        """Upload local file to S3 storage

        Args:
            parent_path (str): Parent path of the file
            file_path (str): Path to local file relative to parent path
            s3_folder (str, optional): Relative parent folder in S3. Defaults to "".

        Returns:
            dict: S3 upload reference
        """

        content_type = self._get_mime_type(file_path)
        if content_type in image_mimetypes:
            return await self._upload_local_file(parent_path, file_path, s3_folder)
        if content_type in model_mimetypes:
            # TODO convert vtk to vtp
            return await self._upload_local_file(parent_path, file_path, s3_folder)
        return await self._upload_local_file(parent_path, file_path, s3_folder)

    async def upload_file(self, upload_file: UploadFile, s3_folder: str = ""):
        """Upload file to S3 storage

        Args:
            upload_file (UploadFile): UploadFile object
            s3_folder (str, optional): Relative parent folder in S3. Defaults to "".

        Returns:
            dict: S3 upload reference
        """
        # if mimetype is image upload image
        if upload_file.content_type in image_mimetypes:
            return await self._upload_image(upload_file, s3_folder)
        if upload_file.content_type in model_mimetypes:
            # TODO convert vtk to vtp
            return await self._upload_file(upload_file, s3_folder)
        return await self._upload_file(upload_file, s3_folder)

    async def delete_file(self, file_path: str):
        """Delete file from S3 storage

        Args:
            file_path (str): Path of the file in S3

        Returns:
            Any: File path if deleted, False otherwise
        """
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

    async def _convert_image(self, upload_file: UploadFile) -> Tuple[BytesIO, BytesIO]:
        """Convert an image to webp format

        Args:
            upload_file (UploadFile): UploadFile object

        Returns:
            Tuple[BytesIO, BytesIO]: Data of webp image and data of original image
        """
        request_object_content = await upload_file.read()
        origin_BytesIo = BytesIO(request_object_content)
        image = Image.open(origin_BytesIo)
        data = BytesIO()
        image.save(data, format="webp", quality=60)
        return (data, origin_BytesIo)

    async def _get_unique_filename(self,
                                   filename: str,
                                   ext: str = "",
                                   s3_folder: str = "") -> Tuple[str, str]:
        """Get unique file path in S3 and file name, change extension if one is provided

        Args:
            filename (str): File name
            ext (str, optional): New file extension. Defaults to "".
            s3_folder (str, optional): Relative parent folder in S3. Defaults to "".

        Returns:
            Tuple[str, str]: File path in S3 and new or original file name
        """
        split_file_name = os.path.splitext(filename)
        ext = ext if ext != "" else split_file_name[1]
        name = split_file_name[0]
        return (f"{s3_folder}/{name}{ext}", f"{name}{ext}")

    async def _upload_image(self, upload_file: UploadFile, s3_folder: str = ""):
        """Upload image to S3, convert to webp if necessary

        Args:
            upload_file (UploadFile): UploadFile object
            s3_folder (str, optional): Relative parent folder in S3. Defaults to "".

        Raises:
            HTTPException: When S3 upload fails

        Returns:
            dict: S3 upload reference
        """
        if upload_file.content_type == "image/webp":
            # no need to convert to webp
            return self._upload_file(upload_file, s3_folder)
        else:
            # convert to bytes
            (data, origin_data) = await self._convert_image(upload_file)

            # Webp converted image
            mimetype = "image/webp"
            (unique_file_name, name) = await self._get_unique_filename(upload_file.filename, ".webp", s3_folder=s3_folder)

            key = f"{config.S3_PATH_PREFIX}{unique_file_name}"
            uploads3 = await self._upload_fileobj(bucket=config.S3_BUCKET,
                                                  key=key,
                                                  data=data.getvalue(),
                                                  mimetype=mimetype)

            if not uploads3:
                raise HTTPException(status_code=500,
                                    detail="Failed to upload image to S3")

            # Original image
            (unique_origin_file_name, origin_name) = await self._get_unique_filename(upload_file.filename, s3_folder=s3_folder)
            key_origin = f"{config.S3_PATH_PREFIX}{unique_origin_file_name}"
            uploads3Origin = await self._upload_fileobj(
                bucket=config.S3_BUCKET,
                key=key_origin,
                data=origin_data.getvalue(),
                mimetype=upload_file.content_type)

            if not uploads3Origin:
                raise HTTPException(status_code=500,
                                    detail="Failed to upload image to S3")

            # response http to be used by the frontend
            return {
                "path": urllib.parse.quote(key),
                "name": name,
                "alt_path": urllib.parse.quote(key_origin),
                "alt_name": origin_name
            }

    async def _upload_file(self, upload_file: UploadFile, s3_folder: str = "") -> dict:
        """Upload file to S3, as is

        Args:
            upload_file (UploadFile): UploadFile object
            s3_folder (str, optional): Relative parent folder in S3. Defaults to "".

        Raises:
            HTTPException: When S3 upload fails

        Returns:
            dict: S3 upload reference
        """
        (filename, name) = await self._get_unique_filename(upload_file.filename, s3_folder=s3_folder)
        key = f"{config.S3_PATH_PREFIX}{filename}"
        uploads3 = await self._upload_fileobj(bucket=config.S3_BUCKET,
                                              key=key,
                                              data=upload_file.file._file,
                                              mimetype=upload_file.content_type)
        if uploads3:
            # response http to be used by the frontend
            return {
                "path": urllib.parse.quote(key),
                "name": name
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to upload file to S3")

    async def _upload_local_file(self, parent_path, file_path: str, s3_folder: str = "") -> dict:
        """Upload file to S3, as is

        Args:
            parent_path (str): Parent path of the file
            file_path (str): Path to local file relative to parent path
            s3_folder (str, optional): Relative parent folder in S3. Defaults to "".

        Raises:
            HTTPException: When S3 upload fails

        Returns:
            dict: S3 upload reference
        """

        (filename, name) = await self._get_unique_filename(file_path, s3_folder=s3_folder)
        key = f"{config.S3_PATH_PREFIX}{filename}"
        with open(os.path.join(parent_path, file_path), 'rb') as file:
            uploads3 = await self._upload_fileobj(bucket=config.S3_BUCKET,
                                                  key=key,
                                                  data=file,
                                                  mimetype=self._get_mime_type(file_path))
        if uploads3:
            # response http to be used by the frontend
            return {
                "path": urllib.parse.quote(key),
                "name": name
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to upload file to S3")

    async def _upload_fileobj(self, data: BytesIO, bucket: str, key: str, mimetype: str) -> bool:
        """Perform the data upload to S3

        Args:
            data (BytesIO): Data to be uploaded
            bucket (str): Destination bucket
            key (str): Path of the obejct in the bucket
            mimetype (str): Object mimetype

        Returns:
            bool: True if upload was successful, False otherwise
        """
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

    def _get_mime_type(self, file_name):
        mime_type, encoding = mimetypes.guess_type(file_name)
        if mime_type is None:
            if file_name.endswith('.vtk') or file_name.endswith('.vtp'):
                mime_type = 'application/x-vtk'
            elif file_name.endswith('.webp'):
                mime_type = 'image/webp'
            else:
                mime_type = 'application/octet-stream'
        return mime_type


s3_client = S3_SERVICE(config.S3_ENDPOINT_PROTOCOL + config.S3_ENDPOINT_HOSTNAME,
                       config.S3_ACCESS_KEY_ID,
                       config.S3_SECRET_ACCESS_KEY, config.S3_REGION)
