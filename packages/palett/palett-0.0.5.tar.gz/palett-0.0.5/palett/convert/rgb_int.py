def rgb_int(rgb):
    r, g, b = rgb
    return ((r & 0xFF) << 16) + ((g & 0xFF) << 8) + (b & 0xFF)
