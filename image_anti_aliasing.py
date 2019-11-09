from PIL import Image


def load_image(path):
    return Image.open(path, 'r').convert('RGB')


def save_image(image, path):
    image.save(path)


def anti_aliase(image, window_side_length):
    assert window_side_length % 2 == 1, "Window side length should be odd"

    image_width, image_height = image.size
    result = Image.new('RGB', (image_width, image_height))
    half_width = window_side_length // 2

    for y in range(image_height):
        for x in range(image_width):
            x_range = __get_window_range(x, half_width, image_width)
            y_range = __get_window_range(y, half_width, image_height)
            window_pixels = [(x, y) for x in x_range for y in y_range]

            pixel_red = sum(__get_color_values(image, window_pixels, 'red')) // len(window_pixels)
            pixel_green = sum(__get_color_values(image, window_pixels, 'green')) // len(window_pixels)
            pixel_blue = sum(__get_color_values(image, window_pixels, 'blue')) // len(window_pixels)
            result.putpixel((x, y), (pixel_red, pixel_green, pixel_blue))
    return result


def __get_color_values(image, pixels_coords, color_name):
    colors_to_tuple_pos = {'r': 0, 'red': 0,
                           'g': 1, 'green': 1,
                           'b': 2, 'blue': 2}
    assert color_name in colors_to_tuple_pos.keys(), "Unknown color"
    return [image.getpixel(pixel)[colors_to_tuple_pos[color_name]] for pixel in pixels_coords]


def __get_window_range(current, window_half_width, length):
    return range(max(current - window_half_width, 0), min(current + window_half_width + 1, length))
