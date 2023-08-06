def bound(rgb):
    r, g, b = rgb
    ma, mi = r, r
    if g > r:
        ma = g
    else:
        mi = g
    if b > ma:
        ma = b
    if b < mi:
        mi = b
    return (
        ma,
        ma + mi,
        ma - mi
    )  # max, sum, dif
