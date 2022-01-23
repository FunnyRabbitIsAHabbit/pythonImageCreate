"""
Project: Create simple images

File: main

Developer: Stanislav Ermokhin

Version: 1.0
"""

import json
import random
from time import time

from PIL import Image

ATTRIBUTES_GROUNDHOG = {'hat', 'gradient_vertical', 'gradient_horizontal',
                        'watch', 'necklace', 'necklace_pendant',
                        'roses_around'}

with open('colors.data') as x:
    y = json.load(x)

COLORS = list(y.keys())


# len(COLORS) = 2331


def olympic_rings():
    """Create list of pixels for field 50x50
    corresponding to Olympic rings depiction (in 1-dimensional array)

    :return tuple"""

    tops_and_bottoms1 = [range(15, 19), range(24, 28), range(33, 37)]
    tops_and_bottoms2 = [range(15, 19), range(25, 29)]
    lefts_and_rights = range(22, 26)
    z_range = (0, 7, 9, 16, 18, 25)
    d_range = (0, 7, 10, 17)
    diag_dots1 = (14, 19, 23, 28, 32, 37)
    diag_dots2 = (14, 19, 24, 29)
    x_base = [(20, y) for y in (x for item in tops_and_bottoms1 for x in item)]
    x_base.extend(((21, y) for y in diag_dots1))
    x_base.extend(((24, y + 4) for y in (x for item in tops_and_bottoms2 for x in item)))
    x_base.extend(((26, y) for y in diag_dots1))
    x_base.extend(((27, y) for y in (x for item in tops_and_bottoms1 for x in item)))
    x_base.extend(((25, y + 4) for y in diag_dots2))
    x_base.extend(((31, y + 4) for y in (x for item in tops_and_bottoms2 for x in item)))
    x_base.extend(((30, y + 4) for y in diag_dots2))
    for z in z_range:
        x_base.extend(((y, 13 + z) for y in lefts_and_rights))
    for d in d_range:
        x_base.extend(((y + 4, 13 + d + 4) for y in lefts_and_rights))

    base = [50 * item[0] + item[1] - 1 for item in x_base]

    return 50, 50, None, base


def change_background(base_pic, new_pixels, find_pixel=None):
    """

    :param base_pic: list as [(a, b, c, d), ..., (..., ..., ..., ...)] of length X
    :param new_pixels: list as [(a, b, c, d), ..., (..., ..., ..., ...)] of length X or
        tuple as (a, b, c, d)
    :param find_pixel: tuple as (a, b, c, d) -- RGBA format
    :return: list as [(a, b, c, d), ..., (..., ..., ..., ...)]
    """

    find_pixel = find_pixel or (0, 0, 0, 0)

    if isinstance(new_pixels, list):
        for pixel_index in range(len(base_pic)):
            if base_pic[pixel_index] == find_pixel:
                base_pic[pixel_index] = new_pixels[pixel_index]

    elif isinstance(new_pixels, tuple):
        for pixel_index in range(len(base_pic)):
            if base_pic[pixel_index] == find_pixel:
                base_pic[pixel_index] = new_pixels

    return base_pic


def old_main(width=None, height=None, pixel_list=None, base_picture_list=None):
    """not Main function

    :return: None
    """

    width = width or 50
    height = height or width
    base_picture_list = base_picture_list or [(None, None)]
    white_rgba_tuple = (250, 250, 250, 250)
    black_rgba_tuple = (0, 0, 0, 250)
    default_rgba_tuple = black_rgba_tuple
    transparent_rgba_tuple = (0, 0, 0, 0)
    pixel_list = pixel_list or [transparent_rgba_tuple
                                for _ in range(width)
                                for _ in range(height)]
    for coordinate in base_picture_list:
        pixel_list[coordinate] = default_rgba_tuple
    img = Image.new('RGBA', (width, height))
    img.putdata(pixel_list)
    img.save(f'image_{str(int(time()))}.png')


def main(width, height, pixels):
    """Main function

    :return: None
    """

    img = Image.new('RGBA', (width, height))
    img.putdata(pixels)
    img = img.resize(size=(1920, 1920), resample=Image.NEAREST)
    img.save(f'images/image_{str(int(time()))}.png')


def get_groundhog_pic_pixels(filename='samples/groundhog.png'):
    """
    Open 'groundhog.png' with PIL, convert to pixel RGBA-values as [(a, b, c, d), ..., (..., ..., ..., ...)]

    :param filename: str
    :return: dict
    """

    im = Image.open('newsamples/groundhog.png', 'r')
    return_lst = list(im.getdata())

    return {'pixels': return_lst, 'width': im.width, 'height': im.height}


def gradient_pixel_plate_vertical(width, height, col1, col2):
    """Return gradient width by height

    :param width: int
    :param height: int
    :param col1: str
    :param col2: str
    :return: list
    """

    base = Image.new('RGBA', (width, height), col1)
    top = Image.new('RGBA', (width, height), col2)
    mask = Image.new('L', (width, height))
    mask_data = list()

    for z in range(height):
        mask_data.extend([int(255 * (z / height))] * width)

    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)

    return list(base.getdata())


if __name__ == '__main__':
    x = get_groundhog_pic_pixels()
    col1, col2 = random.sample(COLORS, 2)
    gradient_field = gradient_pixel_plate_vertical(col1=col1,
                                                   col2=col2,
                                                   width=x['width'],
                                                   height=x['height'])
    x['pixels'] = change_background(x['pixels'],
                                    gradient_field)

    main(**x)
