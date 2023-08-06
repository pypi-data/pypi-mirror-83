from typing import Tuple

from palett.dye.rgb.rgb_ansi import rgb_ansi
from palett.dye.utils import parse_effects
from palett.utils.ansi import CLR_FORE, L, R, SC


def dye(rgb: Tuple[int, int, int], *effects: str):
    head, tail = parse_effects(effects)
    head += SC + rgb_ansi(rgb)
    tail += SC + CLR_FORE
    return lambda text: L + head + R + str(text) + L + tail + R
