from fastapi import APIRouter, UploadFile, status
import os
import aiofiles
from fastapi import APIRouter, status, UploadFile

from ..dependencies import compress_image

from common.resources import response_data
from common.schemas import UniqueResponse
from common.utiles import get_unique_code
from common.exceptions import NotAcceptableError
from config import env_config


router = APIRouter()


@router.post("/upload_image", status_code=status.HTTP_201_CREATED)
async def panel_files_image_post(files: list[UploadFile]):
    names = []
    path = env_config.TMP_IMAGE_ADDRESS

    if not os.path.exists(path):
        os.makedirs(path)

    for file in files:
        if not file.content_type.startswith(('image/jpeg', 'image/jpg', 'image/png', 'image/webp')):
            raise NotAcceptableError(
                'Please send an image as [jpeg,jpg,png,webp]')

        file_size = file.size
        if file_size > env_config.Image_Upload_Size_Limit * 1048576:
            raise NotAcceptableError(
                f"File size is too large. Max size is {env_config.Image_Upload_Size_Limit}MB.")

        file_content = await file.read()

        file_name = f'{get_unique_code()}.{file.filename.split(".")[-1]}'

        if env_config.Image_Compressing:
            compress_image_level = max(
                1, min(100, int(32.77 - 2.7 * (file_size / 1048576))))
            compressed_image_data = await compress_image(file, compress_image_level)

            async with aiofiles.open(f'{path}/{file_name}', 'wb') as out_file:
                await out_file.write(compressed_image_data)
        else:
            async with aiofiles.open(f'{path}/{file_name}', 'wb') as out_file:
                await out_file.write(file_content)

        names.append(file_name)

    return UniqueResponse(response_data.CREATED, filesName=names)
