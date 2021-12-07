from PIL import Image


def join_h(*args: list):
    dst = Image.new('RGB', (sum([img.width for img in args]), args[0].height))
    for img in args:
        dst.paste(img, (sum([im.width for im in args[:args.index(img)]]), 0))
    return dst


def join_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst
