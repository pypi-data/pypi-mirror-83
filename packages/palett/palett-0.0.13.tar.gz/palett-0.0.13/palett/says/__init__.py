from typing import Generator

from pyspare import deco_str
from texting import SP, parenth, LF, bracket
from veho.vector import mutate

from palett import palett_flopper
from palett.structs import Preset


class Says:
    __flopper: Generator
    __effects: tuple
    __roster: dict = {}

    def __init__(self, *effects):
        self.__flopper = palett_flopper(to=Preset.rand)
        self.__effects = effects

    def __call__(self, name, preset=None):
        if name in self.__roster: return self.__roster[name]
        preset = preset or next(self.__flopper)
        dyed_name = deco_str(name, presets=(preset, preset), effects=self.__effects)
        pal = Pal(dyed_name)
        self.__roster[name] = pal
        return pal

    def __getitem__(self, name):
        return self.__call__(name)

    def __getattr__(self, name):
        return self.__call__(name)

    def roster(self, name=None):
        if name: return self.__call__(name).name
        return {name: pal.name for name, pal in self.__roster.items()}


def tab(ind): return SP * (ind << 1)


class Pal:
    name: str = ''
    des: str = ''
    ind: int = 0

    def __init__(self, name):
        self.name = name

    def p(self, words):
        self.des += SP + words
        return self

    def br(self, words):
        self.des += SP + parenth(words)
        return self

    def to(self, someone):
        someone = someone.name if isinstance(someone, Pal) else str(someone)
        self.des += ' -> ' + bracket(someone)
        return self

    def __call__(self, *args, sep=SP, end=LF, file=None):
        signature = bracket(self.name)
        if self.ind: signature = tab(self.ind) + signature
        if self.des:
            signature += self.des
            self.des = ''
        if len(args) and (LF in str(args[0])) and (args := list(args)):
            mutate(args, lambda text: (LF + str(text)).replace(LF, LF + tab(self.ind + 1)))
        print(signature, *args, sep=sep, end=end, file=file)

    @property
    def asc(self):
        self.ind += 1
        return self

    @property
    def desc(self):
        if self.ind: self.ind -= 1
        return self
