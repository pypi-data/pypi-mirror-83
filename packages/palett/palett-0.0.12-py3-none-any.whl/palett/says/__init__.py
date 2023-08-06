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
        preset = next(self.flopper)
        name = deco_str(name, presets=(preset, preset), effects=self.effects)
        return Pal(name)

    def __getitem__(self, name):
        return self.__call__(name)


class Pal:
    name: str

    def __init__(self, name):
        self.name = name

    def __call__(self, *args, sep=' ', end='\n', file=None):
        print(f'[{self.name}]', *args, sep=sep, end=end, file=file)
