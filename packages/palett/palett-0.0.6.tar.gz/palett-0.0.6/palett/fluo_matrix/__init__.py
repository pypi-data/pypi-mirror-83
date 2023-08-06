from veho.enum.matrix_directions import COLUMNWISE, POINTWISE, ROWWISE

from palett.fluo_matrix.fluo_columnwise import fluo_columnwise
from palett.fluo_matrix.fluo_pointwise import fluo_pointwise
from palett.fluo_matrix.fluo_rowwise import fluo_rowwise


def fluo_matrix(mx, direct, presets, effects=None, colorant=False, mutate=False):
    if direct == ROWWISE:
        return fluo_rowwise(mx, presets, effects, colorant, mutate)
    if direct == COLUMNWISE:
        return fluo_columnwise(mx, presets, effects, colorant)
    if direct == POINTWISE:
        return fluo_pointwise(mx, presets, effects, colorant, mutate)
    return mx
