from aryth import constraint

from palett import hex_hsl, hsl_hex, rgb_hsl, hsl_rgb


def hex_toner(hex_color, dh, ds, dl):
    hsl = hex_hsl(hex_color)
    hsl = hsl_toner(hsl, dh, ds, dl)
    return hsl_hex(hsl)


def rgb_toner(rgb, dh, ds, dl):
    hsl = rgb_hsl(rgb)
    hsl = hsl_toner(hsl, dh, ds, dl)
    return hsl_rgb(hsl)


def hsl_toner(hsl, dh, ds, dl):
    hue, saturation, lightness = hsl
    hue = constraint(hue + dh, 0, 360)
    saturation = constraint(saturation + ds, 0, 100)
    lightness = constraint(lightness + dl, 0, 100)
    return hue, saturation, lightness
