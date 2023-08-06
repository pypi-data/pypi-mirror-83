from palett.utils.ansi import FORE, SC


def rgb_ansi(rgb):
    r, g, b = rgb
    return FORE + SC + str(r) + SC + str(g) + SC + str(b)
