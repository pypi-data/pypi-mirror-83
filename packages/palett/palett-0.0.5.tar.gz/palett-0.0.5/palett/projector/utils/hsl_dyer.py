from palett.convert import hsl_rgb
from palett.dyer.rgb import dyer


def hsl_dyer(hsl, *effects): return dyer(hsl_rgb(hsl), *effects)
