from palett.convert.utils.hex import dilute_hex


def hex_int(hex_color: str):
    if hex_color[0] == '#': hex_color = hex_color[1:]
    if len(hex_color) < 6: hex_color = dilute_hex(hex_color)
    return int(hex_color, 16)


'''
@param {string} hex
@returns {number}
'''
