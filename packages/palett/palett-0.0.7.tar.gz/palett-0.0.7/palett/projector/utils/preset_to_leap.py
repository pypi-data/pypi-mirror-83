from palett.projector.utils.parse_hsl import parse_hsl


def preset_to_leap(preset):
    if not preset: return None
    max_hsl = parse_hsl(preset.max)
    min_hsl = parse_hsl(preset.min)
    return color_bound(max_hsl, min_hsl)


def color_bound(max_hsl, min_hsl):
    max_h, max_s, max_l = max_hsl
    min_h, min_s, min_l = min_hsl
    return {
        'min': (min_h, min_s, min_l),
        'dif': (max_h - min_h, max_s - min_s, max_l - min_l)
    }
