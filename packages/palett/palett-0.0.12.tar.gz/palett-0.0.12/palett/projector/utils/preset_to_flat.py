from palett.dye import DyeFactory
from palett.enum.color_spaces import HEX
from palett.structs import Preset


def preset_to_flat(preset: Preset, *effects):
    return DyeFactory(HEX, *effects)(preset.na)
