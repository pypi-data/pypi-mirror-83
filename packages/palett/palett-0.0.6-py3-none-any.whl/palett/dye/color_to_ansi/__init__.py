from palett.convert import hsl_rgb, hex_int
from palett.utils.ansi import FORE, SC


def rgb_ansi(rgb):
    r, g, b = rgb
    return FORE + SC + str(r) + SC + str(g) + SC + str(b)


def hex_ansi(hex_color):
    n = hex_int(hex_color)
    return FORE + SC + str(n >> 16 & 0xFF) + SC + str(n >> 8 & 0xFF) + SC + str(n & 0xFF)


def hsl_ansi(hsl):
    r, g, b = hsl_rgb(hsl)
    return FORE + SC + str(r) + SC + str(g) + SC + str(b)
