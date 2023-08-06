from palett.dyer.hex.hex_ansi import hex_ansi
from palett.dyer.utils import br, parse_effects
from palett.utils.ansi import CLR_FORE


def prep_dyer(*effects):
    head, tail = parse_effects(effects)
    return lambda rgb: lambda text: br(head, hex_ansi(rgb)) + text + br(tail, CLR_FORE)
