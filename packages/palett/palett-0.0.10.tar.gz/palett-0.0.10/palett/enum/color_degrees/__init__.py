accents = [f'accent_{x}' for x in range(4, 0, -1)]
lightens = [f'lighten_{x}' for x in range(5, 0, -1)]
darkens = [f'darken_{x}' for x in range(1, 5)]
base = ['base']
entire = accents + lightens + base + darkens
readable = accents[-3:] + lightens[-3:] + base
