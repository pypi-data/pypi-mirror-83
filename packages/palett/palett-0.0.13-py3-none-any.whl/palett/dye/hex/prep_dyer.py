from palett.dye.hex.hex_ansi import hex_ansi
from palett.dye.utils import br, parse_effects
from palett.utils.ansi import CLR_FORE


def prep_dyer(*effects):
    head, tail = parse_effects(effects)
    return lambda rgb: lambda text: br(head, hex_ansi(rgb)) + text + br(tail, CLR_FORE)
