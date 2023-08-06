from ject import oneself
from pyspare import deco_dict, deco

from palett.convert import hex_rgb, hex_hsl
from palett.enum.color_space import RGB, HSL, HEX
import palett.cards as cards

print(deco(vars(cards)))


def color_picker(color_space):
    if color_space == RGB: return hex_rgb
    if color_space == HSL: return hex_hsl
    if color_space == HEX: return oneself


def palett_table(space, degrees, colors, average, cell_color):
    h = len(degrees)
    w = len(colors)
    # formatter =
    color_picker_0 = color_picker(space)
