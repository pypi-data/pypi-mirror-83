from veho.entries import mutazip, unwind, wind

from palett.fluo.fluo_vector import fluo_vector


def fluo_entries(entries, presets, effects=None, colorant=False, mutate=False):
    (keys, items) = unwind(entries)
    fluo_vector(keys, presets, effects, colorant, mutate=True)
    fluo_vector(items, presets, effects, colorant, mutate=True)
    rendered = wind(keys, items)
    return mutazip(entries, rendered, lambda _, b: b) if mutate else rendered
