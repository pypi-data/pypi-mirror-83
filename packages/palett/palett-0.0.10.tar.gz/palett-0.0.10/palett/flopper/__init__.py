from random import randint, choice

from veho.vector.helper import swap

from palett.cards import grey
from palett.enum.color_degrees import entire
from palett.enum.color_groups import rainbow
from palett.enum.color_spaces import HEX
from palett.tabular import palett_crostab

LIGHTEN = 'lighten'
ACCENT = 'accent'
DARKEN = 'darken'


def degree_to_indice(degree: str):
    i = degree.find('_')
    if i < 0: return randint(14, 16)
    cate = degree[0: i]
    order = int(degree[(i + 1):])
    if cate == LIGHTEN: return 15 - (order - 1) * 3
    if cate == ACCENT: return 14 - (order - 1) * 3
    if cate == DARKEN: return 13 - (order - 1) * 3
    return randint(0, 16)


def palett_flopper(
        space=HEX,
        colors=rainbow,
        degrees=entire,
        default=grey.lighten_1,
        exhausted=True
):
    height, width = len(degrees), len(colors)
    crostab = palett_crostab(space, colors, degrees, dyed=False)
    degrees.sort(key=degree_to_indice, reverse=True)
    i = 0
    while i < height and (j := width):
        head, x = crostab.head[:], degrees[i]
        while (j := j - 1) >= 0:
            y = swap(head, randint(0, j), j)
            yield crostab.cell(x, y)
        i = i + 1
    default_color = default if default else crostab.cell(degrees[0], choice(crostab.head))
    while not exhausted: yield default_color
    return default_color
