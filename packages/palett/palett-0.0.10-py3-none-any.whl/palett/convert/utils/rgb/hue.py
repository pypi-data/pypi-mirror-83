def hue(r, g, b, ma, df):
    if df == 0:
        return 0
    if ma == r:
        return ((g - b) / df + (6 if g < b else 0)) % 6
    if ma == g:
        return (b - r) / df + 2
    if ma == b:
        return (r - g) / df + 4
