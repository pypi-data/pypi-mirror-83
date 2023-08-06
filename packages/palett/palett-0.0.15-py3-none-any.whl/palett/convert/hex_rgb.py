from palett.convert.hex_int import hex_int

'''
@param {string} hex
@returns {number[]}
'''


def hex_rgb(hex_color):
    return (n := hex_int(hex_color)) >> 16 & 0xFF, n >> 8 & 0xFF, n & 0xFF
