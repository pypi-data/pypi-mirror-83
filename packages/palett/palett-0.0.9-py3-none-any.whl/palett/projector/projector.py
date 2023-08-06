from collections import namedtuple
from types import MethodType

from aryth.enum.bound_keys import DIF, MIN
from ject.oneself import to_oneself

from palett.dye import DyeFactory
from palett.enum.color_spaces import HSL
from palett.projector.utils.bound_to_leap import bound_to_leap
from palett.projector.utils.hsl_dyer import hsl_dyer
from palett.projector.utils.leverage import leverage
from palett.projector.utils.preset_to_leap import preset_to_leap

Leverage = namedtuple('Leverage', ['min', 'lever', 'base', 'factory'])


def to_projector(bound, preset, effects):
    if effects is None: effects = ()
    if not bound or not preset: return to_oneself()
    factory = DyeFactory(HSL, *effects)
    bound, leap = bound_to_leap(bound), preset_to_leap(preset)
    if DIF not in bound or not bound[DIF]:
        dye = hsl_dyer(leap[MIN], *effects)
        return lambda _: dye
    return MethodType(projector, Leverage(
        bound[MIN],
        leverage(leap[DIF], bound[DIF]),
        leap[MIN],
        factory
    ))


def projector(self, x):
    lever_h, lever_s, lever_l = self.lever
    base_h, base_s, base_l = self.base
    floor = self.min
    return self.factory((
        scale(x, floor, lever_h, base_h, 360),
        scale(x, floor, lever_s, base_s, 100),
        scale(x, floor, lever_l, base_l, 100),
    ))


def scale(x, floor, lever, base, ceil): return min((max(x, floor) - floor) * lever + base, ceil)
