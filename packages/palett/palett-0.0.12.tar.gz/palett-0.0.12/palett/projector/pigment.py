from intype import is_numeric

from palett.dye import DyeFactory
from palett.enum.color_spaces import HEX
from palett.presets import PLANET
from palett.projector.projector import ProjectorFactory
from palett.projector.utils.bound_to_leap import bound_to_leap


def pigment(bound, preset=PLANET, *effects):
    leap = bound_to_leap(bound)
    default_dye = DyeFactory(HEX, *effects)(preset.na)
    projector = ProjectorFactory(leap, preset, *effects)
    return lambda x: projector(x)(x) if is_numeric(x) else default_dye(x)
