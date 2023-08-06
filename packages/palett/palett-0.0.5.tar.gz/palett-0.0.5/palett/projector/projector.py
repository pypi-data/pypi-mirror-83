from aryth.enum.bound_keys import DIF, MIN
from ject.oneself import to_oneself

from palett.projector.utils.bound_to_leap import bound_to_leap
from palett.projector.utils.hsl_dyer import hsl_dyer
from palett.projector.utils.leverage import leverage
from palett.projector.utils.preset_to_leap import preset_to_leap


def to_projector(bound, preset, effects=None):
    if effects is None: effects = []
    if not bound or not preset: return to_oneself()
    bound, leap = bound_to_leap(bound), preset_to_leap(preset)
    if DIF not in bound or not bound[DIF]:
        dye = hsl_dyer(leap[MIN], *effects)
        return lambda _: dye
    return lambda x: projector(
        x,
        bound[MIN],
        leverage(leap[DIF], bound[DIF]),
        leap[MIN],
        effects
    )


def projector(x, m, lever, base, effects):
    r_h, r_s, r_l = lever
    m_h, m_s, m_l = base
    return hsl_dyer(
        (
            scale(x, m, r_h, m_h, 360),
            scale(x, m, r_s, m_s, 100),
            scale(x, m, r_l, m_l, 100),
        ),
        *effects
    )


def scale(x, min_v, lever, base, ceil):
    return min((max(x, min_v) - min_v) * lever + base, ceil)
