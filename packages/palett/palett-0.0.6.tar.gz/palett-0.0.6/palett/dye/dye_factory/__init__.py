import collections
import types

from palett.dye.color_to_ansi import rgb_ansi, hsl_ansi, hex_ansi
from palett.enum.color_space import RGB, HEX, HSL
from palett.utils.ansi import Effects, SC, R, L, CLR_FORE


def assign_effects(self, effects: tuple):
    for effect in effects:
        if effect in Effects and (effect := Effects[effect]):
            self.head += SC + effect[0]
            self.tail += SC + effect[1]
    return self


def enclose(text): return L + text + R


def dye(self, text): return self.head + str(text) + self.tail


Cut = collections.namedtuple('Cut', ['head', 'tail'])


class DyeFactory:
    ansi: callable
    head: str = ''
    tail: str = ''

    def __init__(self, space, *effects):
        self.ansi = rgb_ansi if space == RGB \
            else hex_ansi if space == HEX \
            else hsl_ansi if space == HSL \
            else rgb_ansi
        if len(effects): assign_effects(self, effects)

    def __call__(self, color):
        head = enclose(self.head + SC + self.ansi(color))
        tail = enclose(self.tail + SC + CLR_FORE)
        return types.MethodType(dye, Cut(head, tail))
