from palett.dye import DyeFactory
from palett.enum.color_spaces import HEX
from palett.presets import PLANET
from palett.projector.projector import ProjectorFactory
from palett.projector.utils import bound_to_leap, preset_to_flat
from intype import is_numeric


def colorant(bound, preset=PLANET, effects=[]):
    leap = bound_to_leap(bound)
    default_dye = DyeFactory(HEX, *effects)(preset.na)
    projector = ProjectorFactory(leap, preset, *effects)
    return lambda x: projector(x) if is_numeric(x) else default_dye
