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
from app.utils.mimetype import zip_mimetypes
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


def unzip_to_temp_directory(zip_file_path):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Open the ZIP file
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            # Extract all contents to the temporary directory
            zip_ref.extractall(temp_dir)

        # Return the path to the temporary directory
        return temp_dir

    except Exception as e:
        print(f"Error during unzip: {e}")
        # Clean up on error
        shutil.rmtree(temp_dir)
        raise


def list_files_recursively(directory, relative=False):
    paths = []
    path = Path(directory)
    for file_path in path.rglob('*'):
        if file_path.is_file():
            if relative:
                paths.append(str(file_path.relative_to(directory)))
            else:
                paths.append(str(file_path))
    return paths


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


@router.get("/{experiment_id}", response_model=ExperimentRead)
async def get_experiment(
    session: AsyncSession = Depends(get_session),
    *,
    experiment_id: int,
) -> ExperimentRead:
    """Get an experiment by id"""
    service = ExperimentsService(session)
    experiment = await service.get(experiment_id)
    return experiment


@router.get("", response_model=list[ExperimentRead])
async def get_experiments(
    response: Response,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[ExperimentRead]:
    """Get all experiments"""
    service = ExperimentsService(session)
    start, end, total_count, experiments = await service.find(filter, sort, range)

    response.headers[
        "Content-Range"
    ] = f"experiments {start}-{end}/{total_count}"
    return experiments


@router.post("", response_model=ExperimentRead)
async def create_experiment(
    experiment: ExperimentCreate = Body(...),
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> ExperimentRead:
    """Creates an experiment"""
    service = ExperimentsService(session)
    experiment = await service.create(Experiment.from_orm(experiment))
    return experiment


@router.put("/{experiment_id}", response_model=ExperimentRead)
async def update_experiment(
    experiment_id: int,
    experiment_update: ExperimentUpdate,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key)
) -> ExperimentRead:
    """Update an experiment by id"""
    service = ExperimentsService(session)
    experiment = await service.patch(experiment_id, experiment_update)
    return experiment


@router.get("/{experiment_id}/files",
            status_code=200,
            description="-- Download experiment assets from S3 as a zip archive --")
async def get_experiment_files(
        experiment_id: int,
        session: AsyncSession = Depends(get_session),
        response: Response = Response(),
):
    service = ExperimentsService(session)
    experiment = await service.get(experiment_id)
    if experiment.files:
        # extract from S3 and archive files
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        folder_name = f"{experiment.id}-{experiment.files['name']}"
        folder_path = os.path.join(temp_dir, folder_name)
        os.makedirs(folder_path)
        await write_files_recursively(folder_path, experiment.files["children"])
        # Create a ZipFile Object
        zip_file_path = os.path.join(temp_dir, f"{folder_name}.zip")
        shutil.make_archive(Path(folder_path), 'zip', Path(folder_path))
        try:
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
    else:
        raise HTTPException(status_code=404, detail="Files not found")


@router.post("/{experiment_id}/files",
             status_code=200,
             dependencies=[Depends(size_checker)])
async def upload_experiment_files(
        experiment_id: int,
        files: UploadFile = File(
            description="Experiment files (zip archive) upload"),
        session: AsyncSession = Depends(get_session),
        api_key: str = Security(get_api_key)):
    service = ExperimentsService(session)
    experiment = await service.get(experiment_id)

    if experiment.files:
        raise HTTPException(
            status_code=400, detail="Experiment already has files")

    if files.content_type not in zip_mimetypes:
        raise HTTPException(
            status_code=415, detail="Only zip archives are allowed")

    # unzip to temp directory
    temp_dir = unzip_to_temp_directory(files.file._file)
    source_dir = temp_dir
    # real zip content is inside the first directory
    dirs = [f.path for f in os.scandir(temp_dir) if f.is_dir()]
    if len(dirs) == 1:
        source_dir = dirs[0]

    # upload files to s3
    current_time = datetime.datetime.now()
    # generate unique name for the files
    unique_name = str(current_time.timestamp()).replace('.', '')
    s3_folder = f"experiments/{experiment_id}/{unique_name}"
    # list files recursively from source directory
    file_relative_paths = list_files_recursively(source_dir, relative=True)
    files = [await s3_client.upload_local_file(source_dir, file_path, s3_folder=s3_folder) for file_path in file_relative_paths]

    # clean up
    shutil.rmtree(temp_dir)

    # update experiment
    # create file tree
    root_node = FileNode(name=unique_name)
    for file in files:
        root_node.add_file(file)
    experiment_update = ExperimentUpdate(
        files=root_node.to_dict(), reference_id=experiment.reference_id)
    experiment = await service.patch(experiment_id, experiment_update)

    return experiment


@router.delete("/{experiment_id}/run_results")
async def delete_experiment_run_results(
    experiment_id: int,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> None:
    """Delete run results of an experiment by id"""
    service = ExperimentsService(session)
    await service.delete_run_results(experiment_id)


@router.delete("/{experiment_id}/files")
async def delete_experiment_files(
    experiment_id: int,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> None:
    """Delete files of an experiment by id"""
    service = ExperimentsService(session)
    await service.delete_files(experiment_id)


@router.delete("/{experiment_id}")
async def delete_experiment(
    experiment_id: int,
    recursive: bool = Query(None),
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> None:
    """Delete an experiment by id"""
    service = ExperimentsService(session)
    await service.delete(experiment_id, recursive)
