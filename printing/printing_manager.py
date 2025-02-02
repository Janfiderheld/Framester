import os
import time

import requests
from PIL import Image

from model import Movie

TARGET_FRONT = "./printing/front/"
TARGET_BACK = "./printing/back/"


def get_front_image(number: int, mov: Movie):
    img = mov.get_img()
    try:
        # Download the original image
        response = requests.get(img, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        ext = os.path.splitext(img)[-1]
        temp_path = f'printing/temp{ext}'
        with open(temp_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        # Crop the image to a fitting size
        filename = os.path.join(TARGET_FRONT, f'{number}{ext}')
        crop_and_resize_image(temp_path, filename)

        # Remove temp image
        os.remove(temp_path)
    except requests.RequestException as e:
        print(f"Error downloading {img}: {e}")


def crop_and_resize_image(temp_path: str, resulting_path: str, target_size=(1122, 822)):
    # targeted card size: 63 x 88 mm => min. 822 x 1122
    with Image.open(temp_path) as img:
        img_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]

        # Resize while keeping aspect ratio
        if img_ratio > target_ratio:
            new_height = target_size[1]
            new_width = int(new_height * img_ratio)
        else:
            new_width = target_size[0]
            new_height = int(new_width / img_ratio)
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        # Crop the center
        left = (new_width - target_size[0]) / 2
        top = (new_height - target_size[1]) / 2
        right = left + target_size[0]
        bottom = top + target_size[1]
        img_cropped = img_resized.crop((left, top, right, bottom))

        # Save the results
        img_cropped.save(resulting_path)


def create_back_image(number: int, mov: Movie):
    pass


def prepare_printing(movies: [Movie]):
    counter = 0
    for m in movies:
        time.sleep(0.5)
        get_front_image(counter, m)
        # create_back_image(counter, m)
        counter += 1
    print("Printing preparation complete.")
