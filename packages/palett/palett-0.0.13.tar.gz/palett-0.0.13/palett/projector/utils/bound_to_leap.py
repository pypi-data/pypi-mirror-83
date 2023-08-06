MAX = 'max'
MIN = 'min'
DIF = 'dif'


def bound_to_leap(bound):
    if hasattr(bound, MIN):
        if hasattr(bound, DIF):
            pass
        elif hasattr(bound, MAX):
            setattr(bound, DIF, (bound.max or 0) - (bound.min or 0))
    elif hasattr(bound, DIF):
        if hasattr(bound, MAX):
            setattr(bound, MIN, (bound.max or 0) - (bound.dif or 0))
        else:
            setattr(bound, MIN, 0)
    elif hasattr(bound, MAX):
        setattr(bound, MIN, 0)
    else:
        setattr(bound, MIN, 0)
        setattr(bound, DIF, 0)
    return bound
