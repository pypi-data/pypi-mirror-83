from palett.convert import hex_hsl


def parse_hsl(color):
    return hex_hsl(color) if isinstance(color, str) else color
