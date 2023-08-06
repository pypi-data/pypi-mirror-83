from palett.dye.rgb.rgb_ansi import rgb_ansi
from palett.dye.utils import br, parse_effects
from palett.utils.ansi import CLR_FORE


def prep_dyer(*effects):
    head, tail = parse_effects(effects)
    return lambda rgb: lambda text: br(head, rgb_ansi(rgb)) + text + br(tail, CLR_FORE)
