from crostab import Crostab
from crostab.convert import samples_to_crostab
from ject import oneself
from texting import CO

import palett.cards as cards
from palett.convert import hex_rgb, hex_hsl
from palett.dye import DyeFactory
from palett.enum.color_groups import entire as entire_colors
from palett.enum.color_degrees import entire as entire_degrees
from palett.enum.color_spaces import HEX, RGB, HSL
from palett.enum.font_effects import INVERSE


def module_to_dict(module): return {k: getattr(module, k) for k in dir(module) if not k.startswith('_')}


card_collection = module_to_dict(cards)


def palett_crostab(
        space=HEX,
        colors=entire_colors,
        degrees=entire_degrees,
        dyed=False
):
    crostab: Crostab = samples_to_crostab(card_collection, side=colors, head=degrees).transpose()
    if space != HEX:
        crostab.mutate(hex_rgb if space == RGB else hex_hsl if space == HSL else oneself)
    if dyed:
        dye_factory = DyeFactory(space, INVERSE)
        crostab.mutate(lambda hex_color: dye_factory(hex_color)(hex_color)) \
            if space == HEX \
            else crostab.mutate(lambda xyz: dye_factory(xyz)(CO.join([f'{v:3.0f}' for v in xyz])))
    return crostab.mutate_head(lambda tx: str(tx).replace('light', 'l').replace('deep', 'd'))
