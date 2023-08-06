MAX = 'max'
MIN = 'min'
DIF = 'dif'


def bound_to_leap(bound):
    if MIN in bound:
        if DIF in bound and bound[DIF] is not None:
            pass
        elif MAX in bound and bound[MAX] is not None:
            bound[DIF] = bound[MAX] - bound[MIN]
    elif DIF in bound:
        if MAX in bound:
            bound[MIN] = bound[MAX] - bound[DIF]
        else:
            bound[MIN] = 0
    elif MAX in bound:
        bound[MIN] = 0
    else:
        bound[MIN] = bound[DIF] = 0
    return bound
