from palett.convert.rgb_int import rgb_int

'''
@param {[number,number,number]} rgb
@returns {string}
'''


# TODO: should convert to upper case

def rgb_hex(rgb): return f'#{rgb_int(rgb):06x}'

# return '#' + rgbToInt(rgb).toString(16).toUpperCase().padStart(6, '0')
