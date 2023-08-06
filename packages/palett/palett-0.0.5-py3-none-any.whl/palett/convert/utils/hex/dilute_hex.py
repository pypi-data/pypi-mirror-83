def dilute_hex(hex_str):
    full = ''
    for char in hex_str:
        full += char + char
    return full
