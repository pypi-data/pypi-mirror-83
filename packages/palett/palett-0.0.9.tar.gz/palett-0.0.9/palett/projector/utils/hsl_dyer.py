from palett.convert import hsl_rgb
from palett.dye.rgb import dye


def hsl_dyer(hsl, *effects): return dye(hsl_rgb(hsl), *effects)
