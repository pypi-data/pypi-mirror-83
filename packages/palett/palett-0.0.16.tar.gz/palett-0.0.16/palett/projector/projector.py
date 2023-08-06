from collections import namedtuple

from palett.dye import DyeFactory
from palett.enum.color_spaces import HSL
from palett.projector.utils import bound_to_leap, leverage, preset_to_leap

Leverage = namedtuple('Leverage', ['min', 'lever', 'base', 'factory'])


class ProjectorFactory:
    floor: float
    lever: tuple
    base: tuple
    factory: DyeFactory

    __slots__ = ('floor', 'lever', 'base', 'factory')

    def __init__(self, bound, preset, *effects):
        value_leap = bound_to_leap(bound)
        color_leap = preset_to_leap(preset)
        self.floor = value_leap.min
        self.lever = leverage(color_leap.dif, value_leap.dif) if value_leap.dif else (0, 0, 0)
        self.base = color_leap.min
        self.factory = DyeFactory(HSL, *effects)
        # if DIF not in value_leap or not value_leap[DIF]:
        #     dye = factory(color_leap[MIN])
        #     return lambda _: dye
        # return MethodType(projector, Leverage(
        #     value_leap[MIN],
        #     leverage(color_leap[DIF], value_leap[DIF]),
        #     color_leap[MIN],
        #     factory
        # ))

    # def __call__(self, bound):
    #     if effects is None: effects = ()
    #     if not bound or not preset: return to_oneself()
    #     factory = DyeFactory(HSL, *effects)
    #     bound, leap = bound_to_leap(bound), preset_to_leap(preset)
    #     if DIF not in bound or not bound[DIF]:
    #         dye = factory(leap[MIN])
    #         return lambda _: dye
    #     return MethodType(projector, Leverage(
    #         bound[MIN],
    #         leverage(leap[DIF], bound[DIF]),
    #         leap[MIN],
    #         factory
    #     ))

    def __call__(self, value):
        floor = self.floor
        lever_h, lever_s, lever_l = self.lever
        base_h, base_s, base_l = self.base
        return self.factory((
            scale(value, floor, lever_h, base_h, 360),
            scale(value, floor, lever_s, base_s, 100),
            scale(value, floor, lever_l, base_l, 100),
        ))


# def projector(conf, x):
#     lever_h, lever_s, lever_l = conf.lever
#     base_h, base_s, base_l = conf.base
#     floor = conf.min
#     return conf.factory((
#         scale(x, floor, lever_h, base_h, 360),
#         scale(x, floor, lever_s, base_s, 100),
#         scale(x, floor, lever_l, base_l, 100),
#     ))


def scale(x, floor, lever, base, ceil): return min((max(x, floor) - floor) * lever + base, ceil)
