from palett.utils.ansi import SC, effects


def parse_effects(input_effects):
    h, t = '', ''
    for ef in input_effects:
        if ef in effects:
            l, r = effects[ef]
            h += SC + l
            t += SC + r
    return h, t
