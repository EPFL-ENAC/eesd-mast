import datetime
import zipfile
import tempfile
import shutil
import os
from urllib.parse import unquote

from pathlib import Path

from fastapi import Depends, Security, APIRouter, Query, Response, Body
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from fastapi.exceptions import HTTPException

from app.db import get_session, AsyncSession
from app.auth import get_api_key
from app.services.files.size import size_checker
from app.utils.mimetype import zip_mimetypes, image_mimetypes
from app.utils.file_nodes import FileNode
from app.services.files.s3client import s3_client
from app.services.experiments.service import ExperimentsService
from app.services.experiments.models import (
    Experiment,
    ExperimentCreate,
    ExperimentRead,
    ExperimentUpdate,
)

router = APIRouter()


@router.get("/models",
            status_code=200,
            description="-- Download experiments numerical model assets as a zip archive --")
async def download_experiments_models(
        filter: str = Query(None),
        session: AsyncSession = Depends(get_session),
        response: Response = Response(),
):
    return await download_experiments_data(
        type="models",
        filter=filter,
        session=session,
        response=response,
    )


@router.get("/files",
            status_code=200,
            description="-- Download experiments test assets as a zip archive --")
async def download_experiments_files(
        filter: str = Query(None),
        session: AsyncSession = Depends(get_session),
        response: Response = Response(),
):
    return await download_experiments_data(
        type="files",
        filter=filter,
        session=session,
        response=response,
    )


async def download_experiments_data(
        type: str,
        filter: str = Query(None),
        session: AsyncSession = Depends(get_session),
        response: Response = Response(),) -> Response:
    service = ExperimentsService(session)
    start, end, total_count, experiments = await service.find(filter, None, None)

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    folder_name = f"experiments-{type}-{datetime.datetime.now().strftime('%Y%m%d')}"
    folder_path = os.path.join(temp_dir, folder_name)
    os.makedirs(folder_path)

    try:
        for experiment in experiments:
            exp: dict = experiment.dict()
            if exp[type] and exp[type]["children"] and len(exp[type]["children"]) > 0:
                # pad building_id up to 3 digits
                exp_folder_name = f"{experiment.building_id}"
                exp_folder_name = '{:0>3}'.format(exp_folder_name)
                # add reference name to folder name
                ref_name = f"{experiment.reference.reference}".replace(
                    " ", "_").replace("(", "").replace(")", "").replace("_et_al.", "")
                exp_folder_name = f"{exp_folder_name}_{ref_name}"
                # make experiment folder path
                experiment_folder_path = os.path.join(
                    folder_path, exp_folder_name)
                os.makedirs(experiment_folder_path)
                # write files recursively
                await write_files_recursively(experiment_folder_path, exp[type]["children"])

        # Create a ZipFile Object
        zip_file_path = os.path.join(temp_dir, f"{folder_name}.zip")
        shutil.make_archive(Path(folder_path), 'zip', Path(folder_path))

        with open(zip_file_path, "rb") as file:
            content = file.read()

        response.headers["Content-Disposition"] = f"attachment; filename={folder_name}.zip"
        response.headers["Content-Type"] = "application/zip"
        response.status_code = 200
        response.body = content
        return response
    finally:
        # Clean up the temporary file
        shutil.rmtree(temp_dir)


async def write_files_recursively(directory, files):
    for file in files:
        file_path = os.path.join(directory, file["name"])
        if file["is_file"]:
            body, content_type = await s3_client.get_file(unquote(file["path"]))
            if body:
                with open(file_path, 'wb') as f:
                    f.write(body)
            else:
                pass
        else:
            os.makedirs(file_path)
            await write_files_recursively(file_path, file["children"])
