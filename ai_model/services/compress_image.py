from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.files.storage import default_storage


def compress_and_save_image(image):
    """Compresses and saves an image to reduce storage usage"""
    img = Image.open(image)
    img = img.convert("RGB")
    img.thumbnail((300, 300))  # Resize to 300x300 pixels

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=70)  # Compress to 70% quality
    buffer.seek(0)

    compressed_image_path = f"compressed_images/{image.name}"
    default_storage.save(compressed_image_path, ContentFile(buffer.read()))

    return compressed_image_path
