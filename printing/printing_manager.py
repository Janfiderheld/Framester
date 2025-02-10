import os
import random
import time
import textwrap

import requests
from PIL import Image, ImageDraw, ImageFont

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


def get_random_color() -> (int, int, int):
    return random.randint(50, 240), random.randint(50, 240), random.randint(50, 240)


def draw_wrapped_text(draw: ImageDraw, text: str, position: (int, int), font: ImageFont, fill="black"):
    lines = textwrap.wrap(text, width=45)
    y_offset = 0
    for line in lines:
        text_size = draw.textbbox((0, 0), line, font=font)
        draw.text((position[0], position[1] + y_offset), line, font=font, fill=fill, anchor="mm")
        y_offset += text_size[3] - text_size[1] + 5


def create_back_image(number: int, mov: Movie, target_size=(1122, 822)):
    bg_color = get_random_color()
    img = Image.new("RGB", target_size, bg_color)
    draw = ImageDraw.Draw(img)

    # Set the text to draw
    year = str(mov.get_year())
    direct = f'Directed By: {mov.get_director()}'
    title = mov.get_name()
    german_title = f'(dt: {mov.get_german_name()})'

    # Load fonts
    try:
        font_year = ImageFont.truetype("arial.ttf", 100)
        font_titles = ImageFont.truetype("arial.ttf", 50)
        font_direct = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font_year = font_direct = font_titles = ImageFont.load_default()

    # Define text positions (centered)
    width, height = target_size
    x_center = width // 2
    y_title = height // 5
    y_ger_title = height // 4 + 50
    y_year = height // 2
    y_direct = height * 3 // 4

    # Draw wrapped text
    draw_wrapped_text(draw, title, (x_center, y_title), font_titles)
    if german_title != "(dt: -)":
        draw_wrapped_text(draw, german_title, (x_center, y_ger_title), font_titles)
    draw_wrapped_text(draw, year, (x_center, y_year), font_year)
    draw_wrapped_text(draw, direct, (x_center, y_direct), font_direct)

    # Save the image
    filename = os.path.join(TARGET_BACK, f'{number}.png')
    img.save(filename)


def prepare_printing(movies: [Movie]):
    counter = 0
    for m in movies:
        time.sleep(0.5)
        get_front_image(counter, m)
        # create_back_image(counter, m)
        counter += 1
    print("Printing preparation complete.")
