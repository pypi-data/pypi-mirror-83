from aryth.bound_vector.duobound import duobound
from aryth.bound_vector.solebound import solebound
from palett.projector import to_projector
from palett.projector.utils.preset_to_flat import preset_to_flat
from veho.vector.enumerate import mapper as mapper_fn, mutate as mutate_fn

SLICE = 'slice'


def fluo_vector(vec, presets, effects=None, colorant=False, mutate=False):
    size = len(vec)
    if not size: return []
    if isinstance(presets, tuple):
        preset_x, preset_y = presets
        info_x, info_y = duobound(vec)
        dye_x, dye_y = to_projector(info_x, preset_x, effects), to_projector(info_y, preset_y, effects)
        unit_to_projector = (to_colorant if colorant else to_pigment)(
            info_x[SLICE], dye_x, info_y[SLICE], dye_y, preset_to_flat(preset_x)
        )
    else:
        preset = presets
        info = solebound(vec)
        dye = to_projector(info, preset, effects)
        unit_to_projector = (to_colorant if colorant else to_pigment)(
            info[SLICE], dye, None, None, preset_to_flat(preset)
        )
    mapper = mutate_fn if mutate else mapper_fn
    return mapper(vec, unit_to_projector)


def to_colorant(vec_x, dye_x, vec_y, dye_y, default_dye):
    return lambda _, i: dye_x(x) \
        if (x := vec_x[i]) is not None \
        else dye_y(y) \
        if vec_y and (y := vec_y[i]) is not None \
        else default_dye


def to_pigment(vec_x, dye_x, vec_y, dye_y, default_dye):
    return lambda some, i: dye_x(x)(some) \
        if (x := vec_x[i]) is not None \
        else dye_y(y)(some) \
        if vec_y and (y := vec_y[i]) is not None \
        else default_dye(some)
