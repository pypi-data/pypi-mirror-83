from palett.convert.utils.rgb import bound, hue

TH = 1000

'''
!dif: dif===0
@param {int} r - [0,255]
@param {int} g - [0,255]
@param {int} b - [0,255]
@returns {[int,float,float]} [Hue([0,360]), Saturation([0,100]), Lightness([0,100])]
'''


def rgb_hsl(rgb):
    r, g, b = rgb
    r /= 255
    g /= 255
    b /= 255
    ma, su, df = bound([r, g, b])
    hu = hue(r, g, b, ma, df) * 60
    sa = 0 if not df else (df / (2 - su)) if su > 1 else df / su
    li = su / 2
    return round(hu), round(sa * TH) / 10.0, round(li * TH) / 10.0
