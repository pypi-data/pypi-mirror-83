from palett.fluo_vector import fluo_vector
from veho.vector import mapper as map_vector, mutate as mut_vector


def fluo_rowwise(mx, presets, effects=None, colorant=False, mutate=False):
    mapper = mut_vector if mutate else map_vector
    return mapper(mx, lambda row: fluo_vector(row, presets, effects, colorant, mutate))
