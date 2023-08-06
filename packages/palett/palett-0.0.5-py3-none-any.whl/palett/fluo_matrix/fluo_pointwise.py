from aryth.bound_matrix.duobound import duobound
from aryth.bound_matrix.solebound import solebound
from palett.projector import to_projector
from palett.projector.utils.preset_to_flat import preset_to_flat
from veho.matrix import size
from veho.matrix.enumerate import mapper as mapper_fn, mutate as mutate_fn

SLICE = 'slice'


def fluo_pointwise(mx, presets, effects=None, colorant=False, mutate=False):
    h, w = size(mx)
    if not h or not w: return [[]]
    if isinstance(presets, tuple):
        preset_x, preset_y = presets
        info_x, info_y = duobound(mx)
        dye_x, dye_y = to_projector(info_x, preset_x, effects), to_projector(info_y, preset_y, effects)
        unit_to_projector = (to_colorant if colorant else to_pigment)(
            info_x[SLICE], dye_x, info_y[SLICE], dye_y, preset_to_flat(preset_x)
        )
    else:
        preset = presets
        info = solebound(mx)
        dye = to_projector(info, preset, effects)
        unit_to_projector = (to_colorant if colorant else to_pigment)(
            info[SLICE], dye, None, None, preset_to_flat(preset)
        )
    mapper = mutate_fn if mutate else mapper_fn
    return mapper(mx, unit_to_projector)


def to_colorant(mx_x, dye_x, mx_y, dye_y, default_dye):
    return lambda _, i, j: dye_x(x) \
        if (x := mx_x[i][j]) is not None \
        else dye_y(y) \
        if mx_y and (y := mx_y[i][j]) is not None \
        else default_dye


def to_pigment(mx_x, dye_x, mx_y, dye_y, default_dye):
    return lambda some, i, j: dye_x(x)(some) \
        if (x := mx_x[i][j]) is not None \
        else dye_y(y)(some) \
        if mx_y and (y := mx_y[i][j]) is not None \
        else default_dye(some)
