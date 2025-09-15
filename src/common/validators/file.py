import io

from fastapi import UploadFile
from PIL import Image

from common.errors.base import ImageValidationError


async def validate_image(
    file: UploadFile,
    max_size_mb: int = 2,
    min_dim: int = 128,
    max_dim: int = 2048,
):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise ImageValidationError(
            message="Invalid file type",
            allowed_types=["jpeg", "png", "webp"],
        )

    contents = await file.read()
    if len(contents) > max_size_mb * 1024 * 1024:
        raise ImageValidationError(message="File too large", max_size_mb=max_size_mb)

    image = Image.open(io.BytesIO(contents))
    width, height = image.size

    if width < min_dim or height < min_dim:
        raise ImageValidationError(
            message="Image too small",
            min_dim=min_dim,
            actual_dim=(width, height),
        )

    if width > max_dim or height > max_dim:
        raise ImageValidationError(
            message="Image too large",
            max_dim=max_dim,
            actual_dim=(width, height),
        )

    return image
