from fastapi import APIRouter, UploadFile, status
import os
import aiofiles
from fastapi import APIRouter, status, UploadFile


from common.resources import response_data
from common.schemas import UniqueResponse
from common.utiles import get_unique_code
from common.exceptions import NotAcceptableError
from config import env_config


router = APIRouter()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def panel_files_image_post(files: list[UploadFile]):
    names = []
    path = env_config.TMP_FILES_ADDRESS

    if not os.path.exists(path):
        os.makedirs(path)

    for file in files:
        if not file.content_type == 'application/zip':
            raise NotAcceptableError('Please send a zip file')

        file_size = file.size
        if file_size > env_config.Upload_Size_Limit * 1048576:
            raise NotAcceptableError(
                f"File size is too large. Max size is {env_config.Image_Upload_Size_Limit}MB.")

        file_content = await file.read()

        file_name = f'{get_unique_code()}.{file.filename.split(".")[-1]}'

        async with aiofiles.open(f'{path}/{file_name}', 'wb') as out_file:
            await out_file.write(file_content)

        names.append(file_name)

    return UniqueResponse(response_data.CREATED, filesName=names)
