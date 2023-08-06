from palett.fluo.fluo_vector import fluo_vector
from veho.columns import mapper
from veho.matrix import transpose


def fluo_columnwise(mx, presets, effects=None, colorant=False):
    return transpose(mapper(mx, lambda col: fluo_vector(col, presets, effects, colorant, mutate=True)))
