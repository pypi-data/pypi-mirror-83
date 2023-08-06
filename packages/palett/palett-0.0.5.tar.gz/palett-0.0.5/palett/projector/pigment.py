from palett.presets import PLANET
from palett.projector.projector import to_projector
from palett.projector.utils.bound_to_leap import bound_to_leap
from palett.projector.utils.preset_to_flat import preset_to_flat
from intype import is_numeric


def pigment(bound, preset=PLANET, effects=[]):
    leap = bound_to_leap(bound)
    default_dye = preset_to_flat(preset)
    projector = to_projector(leap, preset, effects)
    return lambda x: projector(x)(x) if is_numeric(x) else default_dye(x)
