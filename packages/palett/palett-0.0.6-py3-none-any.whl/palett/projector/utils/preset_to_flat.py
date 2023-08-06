from palett.structs import Preset
from palett.projector.utils.hsl_dyer import hsl_dyer
from palett.projector.utils.parse_hsl import parse_hsl


def preset_to_flat(preset: Preset):
    return hsl_dyer(parse_hsl(preset.na))
