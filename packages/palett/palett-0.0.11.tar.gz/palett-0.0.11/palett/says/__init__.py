from typing import Generator

from foba.dicts.dict_strings import dict_collection
from pyspare import deco_dict, deco_str

from palett import palett_flopper
from palett.enum.font_effects import BOLD
from palett.structs import Preset


class Says:
    flopper: Generator
    effects: tuple

    def __init__(self, *effects):
        self.flopper = palett_flopper(to=Preset.rand)
        self.effects = effects

    def __call__(self, name):
        return Pal(deco_str(name, presets=next(self.flopper), effects=self.effects))


class Pal:
    name: str

    def __init__(self, name):
        self.name = name

    def __call__(self, content):
        print(f'[{self.name}]', content)


def test():
    name, lex = dict_collection.flop_shuffle(7)
    print(name, deco_dict(lex))
    says = Says(BOLD)
    for key, value in lex.items():
        says(key)(value)


test()
