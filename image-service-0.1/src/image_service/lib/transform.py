import io

from PIL import Image, ImageOps

from image_service.core.logging import logger


async def resize_image(file, width, height, quality=85):
    logger.debug(f"resizing {file} to {width} x {height}")
    dimensions = (int(width), int(height))

    with Image.open(file) as im:
        im = ImageOps.exif_transpose(im)

        in_mem_file = io.BytesIO()

        im.thumbnail(dimensions)

        im.save(in_mem_file, format="JPEG", quality=quality)
        in_mem_file.seek(0)

        return in_mem_file
