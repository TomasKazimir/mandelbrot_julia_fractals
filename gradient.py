import numpy as np
import random


def get_gradient_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T


def get_gradient_3d(width, height, start_list, stop_list, is_horizontal_list):
    result = np.zeros((height, width, len(start_list)), dtype=float)

    for i, (start, stop, is_horizontal) in enumerate(
        zip(start_list, stop_list, is_horizontal_list)
    ):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)

    return result


def random_gradient(size):
    width, height = size

    color1 = (
        random.uniform(0, 1),
        random.uniform(0, 1),
        random.uniform(0, 1),
    )
    color2 = (
        random.uniform(0, 1),
        random.uniform(0, 1),
        random.uniform(0, 1),
    )

    return get_gradient_3d(width, height, color1, color2, (True, False, False))


# print(list(get_gradient_2d(0, 255, 10, 1, True)[0]))
# from PIL import Image

# g = random_gradient((50, 25))
# print(g)
# Image.fromarray(np.uint8(g)).show()
