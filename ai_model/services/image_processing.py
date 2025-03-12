import cv2
import numpy as np
from PIL import Image

default_image_size = (256, 256)


def preprocess_image(image_path):
    """Processes an image to make it suitable for model prediction."""
    img = Image.open(image_path)
    img = img.resize((224, 224))  # Assuming model requires 224x224
    img_array = np.array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array
