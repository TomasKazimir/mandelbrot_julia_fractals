import colorsys
import csv
import math
import os
import random

import matplotlib.colors as mc
from PIL import Image, ImageDraw

from gradient import random_gradient


def iter_function(z, c, max_abs, max_iter):
    """
    iterative function to determine the color of each pixel
    z are the pixel coordinates represented as a complex number
    c is an 'defining' complex number - every complex number will generate a different julia set fractal
    """
    n = 1
    while abs(z) <= max_abs and n < max_iter:
        # cubic:
        #  z = z ** 3 + c
        # classic:
        z = z ** 2 + c
        n += 1
    return n, z


def juliaset(
    c_origin: complex,
    zoom: float,
    pos: tuple,
    img_size: tuple,
    max_abs: float,
    max_iter: int,
    color_mode: str,
    base_or_exp: float,
    const: float,
    scale: float,
    bg_aggressivity: float,
    bg_grad: list,
    palette: list,
    save_path: str,
):

    # img resolution
    WIDTH, HEIGHT = img_size
    ratio = HEIGHT / WIDTH

    # Plot window
    X, Y = pos
    ZOOM = zoom

    # each julia set lies in the complex plane between -1.5; 1.5 on the real axis and -1.5; 1.5 on the imaginary axis
    # real values:
    RE_START = X - 1.5 / 2 ** ZOOM
    RE_END = X + 1.5 / 2 ** ZOOM
    # imaginary values:
    IM_START = Y + 1.5 * ratio / 2 ** ZOOM
    IM_END = Y - 1.5 * ratio / 2 ** ZOOM

    im = Image.new("RGB", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(im)
    for x in range(WIDTH):
        for y in range(HEIGHT):

            z = complex(
                RE_START + (x / WIDTH) * (RE_END - RE_START),
                IM_START + (y / HEIGHT) * (IM_END - IM_START),
            )

            iter_reached, z = iter_function(z, c_origin, max_abs, max_iter)
            if iter_reached / max_iter > bg_aggressivity:
                # coloring
                if color_mode == "power":
                    distance = (iter_reached + 1) / (max_iter + 1)
                    color = powerColor(distance, base_or_exp, const, scale)
                elif color_mode == "palette":
                    color = pick_color(iter_reached, z, palette)
                else:
                    distance = (iter_reached + 1) / (max_iter + 1)
                    color = logColor(distance, base_or_exp, const, scale)
            else:
                color = adjust_lightness([val for val in bg_grad[y][x]])
                color = tuple(round(i * 255) for i in color)
            # color = int(iter_reached / max_iter * 255)
            draw.point([x, y], (color))
    # im.show()
    im.save(f"{save_path};c{c},z{ZOOM},i{max_iter}.png")


def logColor(distance, base, const, scale):
    color = -1 * math.log(distance, base)
    rgb = colorsys.hsv_to_rgb(const + scale * color, 0.8, 0.9)
    return tuple(round(i * 255) for i in rgb)


def powerColor(distance, exp, const, scale):
    color = distance ** exp
    rgb = colorsys.hsv_to_rgb(const + scale * color, 1 - 0.6 * color, 0.9)
    rgb = adjust_lightness(rgb, 0.8)
    return tuple(round(i * 255) for i in rgb)


def pick_color(n, z, palette):
    # nsmooth = n + 1 - math.log(abs(math.log(abs(z) + 0.001))) / math.log(2)
    # if nsmooth > iter_limit - 1:
    #     nsmooth = iter_limit - 1
    # nsmooth = abs(nsmooth / iter_limit * len(palette) - 1)
    # return int("0x" + palette[round(nsmooth)], 16)

    return int("0x" + palette[n % len(palette)], 16)


def adjust_lightness(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


if __name__ == "__main__":
    img_size = (500, 500)
    c = -0.76249734475934 - 0.089757341313j
    # c = -0.1 - 0.96j
    # c = -0.6625 - 0.45j
    zoom = 0
    pos = (0, 0)  # fractal offset
    max_abs = 10
    max_iter = 500
    color_mode = "palette"  # must be 'palette', 'power', or 'log'
    base_or_exp, const, scale = 0.18, 3.28, 1.53  # fractal color constants

    # background
    bg_grad = random_gradient(img_size)
    bg_aggressivity = 0.0  # 0 to 1

    # load color palletes
    with open("newpalettes.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        palettes = list(reader)
    palette = random.choice(palettes)
    palette = palette + list(reversed(palette))

    # batch variables:
    batch_size = 10  # size of the batch
    batch_dir = "new_batch_{}".format(
        random.randint(1, 1000)
    )  # name of a folder where to save the batch
    zoom_increase = 0.2  # zoom-in by this value every time
    if not os.path.exists(batch_dir):  # create the batch_dir if it does not exist
        os.mkdir(batch_dir)

    # log file
    with open(f"{batch_dir}/log.txt", "a+") as log_file:
        log_file.write(
            "index: function args: c, zoom, pos, img_size, max_abs, max_iter, color_mode, base_or_exp, const, scale, bg_aggressivity\n"
        )

    # batch loop
    for i in range(batch_size):
        index = "0" * (3 - len(str(i))) + str(i)
        save_path = batch_dir + "/" + index
        with open(f"{batch_dir}/log.txt", "a+") as log_file:
            log_file.write(
                f"{index}:  juliaset args: {c, zoom, pos, img_size, max_abs, max_iter, color_mode, base_or_exp, const, scale, bg_aggressivity}\n"
            )
        juliaset(
            c,
            zoom,
            pos,
            img_size,
            max_abs,
            max_iter,
            color_mode,
            base_or_exp,
            const,
            scale,
            bg_aggressivity,
            bg_grad,
            palette,
            save_path,
        )
        bg_grad = random_gradient(img_size)
        zoom = round(zoom + zoom_increase, 2)
        color_mode = random.choice(["power", "power"])
        palette = random.choice(palettes)
        base_or_exp = round(random.uniform(0.1, 0.3), 2)
        const = round(random.uniform(0, 0), 2)
        scale = round(random.uniform(2.2, 2.8), 2)
