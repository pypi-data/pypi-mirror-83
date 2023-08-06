from palett.convert.hex_rgb import hex_rgb
from palett.convert.rgb_hsl import rgb_hsl


def hex_hsl(hex_color): return rgb_hsl(hex_rgb(hex_color))
