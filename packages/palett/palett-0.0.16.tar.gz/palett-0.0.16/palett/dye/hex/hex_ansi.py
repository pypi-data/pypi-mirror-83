from palett.convert import hex_int
from palett.utils.ansi import FORE, SC


def hex_ansi(hex_color):
    val = hex_int(hex_color)
    return FORE + SC + str(val >> 16 & 0xFF) + SC + str(val >> 8 & 0xFF) + SC + str(val & 0xFF)
