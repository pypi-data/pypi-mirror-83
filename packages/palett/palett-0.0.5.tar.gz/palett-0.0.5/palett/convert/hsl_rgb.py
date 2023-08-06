from palett.convert.utils.hsl import hf

'''
 * @param {number} h
 * @param {number} s
 * @param {number} l
 * @returns {number[]}
'''


def hsl_rgb(hsl):
    hu, sa, li = hsl
    sa /= 100
    li /= 100
    a = sa * min(li, 1 - li)
    r = hf(0, hu, a, li)
    g = hf(8, hu, a, li)
    b = hf(4, hu, a, li)
    return round(r * 0xFF), round(g * 0xFF), round(b * 0xFF)
