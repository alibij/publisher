import io
from PIL import Image


async def compress_image(file, quality=25):
    with Image.open(file.file) as img:
        img = img.convert("RGB")
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality)
        output.seek(0)
        return output.getvalue()
