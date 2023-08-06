from typing import Generator

from foba.dicts.dict_strings import dict_collection
from pyspare import deco_dict

from palett import palett_flopper, DyeFactory
from palett.enum.color_spaces import HEX
from palett.enum.font_effects import BOLD


class Says:
    flopper: Generator
    dye_factory: DyeFactory = DyeFactory(HEX, BOLD)

    def __init__(self):
        self.flopper = palett_flopper()
        pass

    def __call__(self, name):
        hex_color = next(self.flopper)
        dye = self.dye_factory(hex_color)
        return Pal(dye(name))


class Pal:
    name: str

    def __init__(self, name):
        self.name = name

    def __call__(self, content):
        print(f'[{self.name}]', content)


def test():
    name, lex = dict_collection.flop_shuffle(7)
    print(name, deco_dict(lex))
    says = Says()
    for key, value in lex.items():
        says(key)(value)


test()
