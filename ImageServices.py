from datetime import datetime , timedelta
import requests
import os
from PIL import Image, ImageOps


def download_the_images(images_name) :
    paths = []
    i = 0
    for name in images_name :
        current_time = (datetime.now() +timedelta(seconds=i)).strftime("%Y%m%d_%H%M%S")
        local_image_path = f"image_{current_time}.jpg"
        response = requests.get(name)
        if response.status_code == 200:
            with open(local_image_path, 'wb') as f:
                f.write(response.content)
                paths.append(local_image_path)
        i = i+1
    return paths


def delete_the_images(images_name) :
    for name in images_name :
        os.remove(name)

# Function to add padding to adjust image aspect ratio
def add_padding(image_path):
    image = Image.open(image_path)
    width, height = image.size
    target_aspect_ratio = 0.8

    if width / height > target_aspect_ratio:
        new_height = int(width / target_aspect_ratio)
        padding_top = (new_height - height) // 2
        padding_bottom = new_height - height - padding_top
        padding = (0, padding_top, 0, padding_bottom)
    else:
        new_width = int(height * target_aspect_ratio)
        padding_left = (new_width - width) // 2
        padding_right = new_width - width - padding_left
        padding = (padding_left, 0, padding_right, 0)

    padded_image = ImageOps.expand(image, padding, fill='white')
    padded_image.save(image_path)