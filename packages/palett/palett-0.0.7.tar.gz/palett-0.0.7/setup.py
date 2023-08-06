# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['palett',
 'palett.cards',
 'palett.convert',
 'palett.convert.utils',
 'palett.convert.utils.hex',
 'palett.convert.utils.hsl',
 'palett.convert.utils.rgb',
 'palett.dye',
 'palett.dye.color_to_ansi',
 'palett.dye.dye_factory',
 'palett.dye.hex',
 'palett.dye.rgb',
 'palett.dye.utils',
 'palett.enum',
 'palett.enum.color_cards',
 'palett.enum.color_degrees',
 'palett.enum.color_groups',
 'palett.enum.color_spaces',
 'palett.enum.font_effects',
 'palett.flopper',
 'palett.fluo',
 'palett.fluo.fluo_entries',
 'palett.fluo.fluo_matrix',
 'palett.fluo.fluo_vector',
 'palett.palett_table',
 'palett.presets',
 'palett.projector',
 'palett.projector.utils',
 'palett.structs',
 'palett.structs.card',
 'palett.structs.preset',
 'palett.tabular',
 'palett.utils',
 'palett.utils.ansi']

package_data = \
{'': ['*']}

install_requires = \
['aryth>=0.0.5',
 'crostab>=0.0.6',
 'intype>=0.0.2',
 'ject>=0.0.1',
 'pyspare>=0.0.6',
 'veho>=0.0.7']

setup_kwargs = {
    'name': 'palett',
    'version': '0.0.7',
    'description': 'pretty text for command line',
    'long_description': "## palett\n##### pretty text for command line\n\n### Usage\n```python\n\nfrom palett.fluo.fluo_vector import fluo_vector\nfrom palett.presets import FRESH, PLANET\n\nvectorCollection = [\n    [],\n    ['Xx', 'Yy', 'Zz', 'e', 'd', 'c', '-', '1', 2, 3],\n    [1, 1, 2, 3, 5, []],\n    ['a', 'b', 'c', 'd', 'e'],\n    ['beijing', 'shanghai', 'wuhan', 'xiamen', 'changsha']\n]\n\n\ndef test():\n    COMMA_SPACE = ', '\n    for vec in vectorCollection:\n        fluoed = fluo_vector(vec, (FRESH, PLANET))\n        print(f'[{COMMA_SPACE.join(fluoed)}]')\n\n\ntest()\n```",
    'author': 'Hoyeung Wong',
    'author_email': 'hoyeungw@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydget/texting.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
