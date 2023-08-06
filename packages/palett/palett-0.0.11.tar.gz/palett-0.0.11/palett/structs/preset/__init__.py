from dataclasses import dataclass
from random import randint

from aryth import constraint

from palett.convert import hsl_hex, hex_hsl
from palett.toner import hsl_toner


@dataclass
class Preset:
    max: str
    min: str
    na: str

    @staticmethod
    def rand(hex_color):
        vale = hex_hsl(hex_color)
        peak = hsl_toner(vale, randint(-12, 12), randint(-5, 10), randint(6, 18))
        hue, saturation, lightness = vale
        na = (
            reverse_hue(hue),
            constraint(saturation - 32, 5, 90),
            constraint(lightness + 24, 40, 96)
        )
        return Preset(hsl_hex(vale), hsl_hex(peak), hsl_hex(na))


def reverse_hue(hue):
    hue += 180
    return hue - 360 if hue > 360 else hue + 360 if hue < 0 else hue
