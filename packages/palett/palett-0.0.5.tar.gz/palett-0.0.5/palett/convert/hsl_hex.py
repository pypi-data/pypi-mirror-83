from palett.convert.hsl_rgb import hsl_rgb
from palett.convert.rgb_hex import rgb_hex


def hsl_hex(hsl): return rgb_hex(hsl_rgb(hsl))
