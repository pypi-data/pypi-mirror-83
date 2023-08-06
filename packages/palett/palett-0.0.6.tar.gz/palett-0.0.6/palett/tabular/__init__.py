import palett.cards as cards


def module_to_dict(module): return {k: getattr(module, k) for k in dir(module) if not k.startswith('_')}


card_collection = module_to_dict(cards)


def palett_crostab(colors=None, degrees=None, dyed=False):
    crostab = samples_to_crostab(card_collection, side=colors, head=degrees)

