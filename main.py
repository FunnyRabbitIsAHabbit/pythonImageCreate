"""
Project: Create simple images

File: main

Developer: Stanislav Ermokhin

Version: 1.0
"""

import json
import random
from statistics import mean

from PIL import Image, ImageColor

ATTRIBUTES_GROUNDHOG = {'tux', 'hat_baseball', 'hat_flat', 'hat_top',
                        'hat_wide', 'gradient', 'watch',
                        'necklace', 'necklace_pendant',
                        'roses_around_left', 'roses_around_right'}

TRANSPARENT = (0, 0, 0, 0)
BLACK = (255, 255, 255, 255)

attributes_compatibility = {x: [y for y in ATTRIBUTES_GROUNDHOG
                                if 'hat' not in y]
                            for x in ATTRIBUTES_GROUNDHOG
                            if 'hat' in x}
attributes_compatibility.update({x: [y for y in ATTRIBUTES_GROUNDHOG
                                     if 'necklace' not in y]
                                 for x in ATTRIBUTES_GROUNDHOG
                                 if 'necklace' in x})

with open('colors.data') as x:
    y = json.load(x)

colors = list(y.keys())


# len(colors) = 2331


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


def main(width, height, pixels, name):
    """Main function

    :return: None
    """

    img = Image.new('RGBA', (width, height))
    img.putdata(pixels)
    img = img.resize(size=(1920, 1920), resample=Image.NEAREST)
    img.save(f'images/{name}.png')


def choose_background(base, color1, gradient=False, color2=None):
    """

    :param base: dict
    :param color1: str
    :param gradient: bool (default False)
    :param color2: str (optional)
    :return: dict (base_with_background)
    """

    if gradient:
        gradient_field = gradient_pixel_plate_vertical(col1=color1,
                                                       col2=color2,
                                                       width=base['width'],
                                                       height=base['height'])
        base['pixels'] = change_background(base['pixels'],
                                           gradient_field)

    else:
        col1 = Image.new('RGBA', (1, 1), color1).getdata()[0]
        base['pixels'] = change_background(base['pixels'],
                                           col1)

    return base


def set_attributes(base_with_background, attributes_pixels):
    """

    :param base_with_background: dict (generated by 'choose_background')
    :param attributes_pixels: list (all attributes inplace)
    :return: dict (picture to be resized and saved)
    """

    to_return = base_with_background
    if attributes_pixels is not None:
        for i in range(len(attributes_pixels)):
            if attributes_pixels[i] != TRANSPARENT:
                to_return['pixels'][i] = attributes_pixels[i]

    return to_return


def generate_and_save_picture(name, base_with_background, attributes_pixels):
    """

    :param name: name.png will be the picture's name upon saving
    :param base_with_background: dict (generated by 'choose_background')
    :param attributes_pixels: attributes_pixels: list (all attributes inplace)
    :return:
    """

    base_with_attributes = set_attributes(base_with_background,
                                          attributes_pixels)
    main(name=name,
         **base_with_attributes)


def restrictions(pixel_main, pixel_in_test):
    """

    :param pixel_main: tuple
    :param pixel_in_test: tuple
    :return: bool
    """

    is_restricted = False
    pixel_main = list(pixel_main)
    pixel_in_test = list(pixel_in_test)
    pixel_in_test.pop(-1)
    pixel_main.pop(-1)

    if not (pixel_main[0] == pixel_main[1] == pixel_main[2]):
        maximum = max(pixel_main)
        minimum = min(pixel_main)
        maximum_test = max(pixel_in_test)
        minimum_test = min(pixel_in_test)
        if pixel_in_test.index(minimum_test) == pixel_main.index(minimum) and \
                pixel_in_test.index(maximum_test) == pixel_main.index(maximum) and \
                mean(pixel_in_test) <= mean(pixel_main):
            is_restricted = True
    else:
        if pixel_in_test[0] == pixel_in_test[1] == pixel_in_test[2]:
            is_restricted = True

    return is_restricted


def test_for_multiple_colors(pixels):
    """

    :param pixels: list of pixels as [(r, g, b, a), ...]
    :return: tuple as (bool, list)
    """

    bool_multiple = False
    pixels_set = set(pixels)
    if len(pixels_set) > 2 and TRANSPARENT in pixels_set or \
            len(pixels_set) > 1 and TRANSPARENT not in pixels_set:
        bool_multiple = True

    pixels_set.discard(TRANSPARENT)

    return bool_multiple, list(pixels_set)


def random_color():
    """

    :return: tuple
    """

    col = random.sample(colors, 1)[0]
    new_pixel = list(ImageColor.getrgb(col))
    new_pixel.extend([255])

    return tuple(new_pixel)


def random_color_set(attribute_pixels):
    """

    :param attribute_pixels: list
    :return: list-||-
    """

    tested = test_for_multiple_colors(attribute_pixels)
    changes = dict()
    colors_to_change = tested[1]

    for pixel in colors_to_change:
        col = random_color()
        changes[pixel] = col
        while not restrictions(pixel, col):
            col = random_color()
            changes[pixel] = col

    for i in range(len(attribute_pixels)):
        if attribute_pixels[i] != TRANSPARENT:
            attribute_pixels[i] = changes[attribute_pixels[i]]

    return attribute_pixels


def get_pic(filename='newsamples/groundhog.png'):
    """
    Open 'groundhog.png' with PIL, convert to pixel RGBA-values as [(a, b, c, d), ..., (..., ..., ..., ...)]

    :param filename: str
    :return: dict
    """

    im = Image.open(filename, 'r')
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


def combine_attributes(collection):
    """

    :param collection: list of lists
    :return: list
    """

    to_return = list()

    if bool(collection):
        to_return = collection[0]

        for attribute_list in collection:
            for i in range(len(attribute_list)):
                if attribute_list[i] != TRANSPARENT:
                    to_return[i] = attribute_list[i]

    return to_return


if __name__ == '__main__':
    y = get_pic()

    atts = list()
    n = 10
    n_pictures = 10
    for _ in range(n):
        for i in range(1, len(ATTRIBUTES_GROUNDHOG) + 1):
            samp = random.sample(ATTRIBUTES_GROUNDHOG, i)
            atts.append(samp)

    atts = random.sample(atts, n_pictures)

    for lst in atts:
        while len([x for x in lst
                   if 'hat' in x]) > 1:
            for item in [x for x in lst
                         if 'hat' in x]:
                lst.pop(lst.index(item))
        while len([x for x in lst
                   if 'necklace' in x]) > 1:
            for item in [x for x in lst
                         if 'necklace' in x]:
                lst.pop(lst.index(item))

    for a in range(len(atts)):
        if 'tux' in atts[a]:
            if atts[a][-1] != 'tux':
                i1, i2 = atts[a].index('tux'), -1
                atts[a][i2], atts[a][i1] = atts[a][i1], atts[a][i2]

        collected_attributes = list()
        if 'gradient' not in atts[a]:
            color = random.sample(colors, 1)[0]
            base_with_back = choose_background(y, color1=color)
        else:
            col1, col2 = random.sample(colors, 2)
            base_with_back = choose_background(y, gradient=True,
                                               color1=col1, color2=col2)

        for attribute in atts[a]:
            if attribute != 'gradient':
                attribute_pic_dict = get_pic(f'newsamples/{attribute}.png')
                if 'tux' not in attribute:
                    to_collect = random_color_set(attribute_pic_dict['pixels'])
                else:
                    to_collect = attribute_pic_dict['pixels']
                collected_attributes.append(to_collect)

        all_atts_together = combine_attributes(collected_attributes)
        generate_and_save_picture(name=a + 1,
                                  base_with_background=base_with_back,
                                  attributes_pixels=all_atts_together)
