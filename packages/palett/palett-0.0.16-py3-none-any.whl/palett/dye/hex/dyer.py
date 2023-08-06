from palett.dye.hex.hex_ansi import hex_ansi
from palett.dye.utils import parse_effects
from palett.utils.ansi import CLR_FORE, L, R, SC


def dyer(hex_color: str, *effects: str):
    head, tail = parse_effects(effects)
    head += SC + hex_ansi(hex_color)
    tail += SC + CLR_FORE
    return lambda text: L + head + R + str(text) + L + tail + R
