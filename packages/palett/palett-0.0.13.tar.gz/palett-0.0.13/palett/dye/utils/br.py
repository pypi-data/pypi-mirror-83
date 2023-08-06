from typing import List

from palett.utils.ansi import L, R, SC


def br(*texts: List[str]): return L + SC.join(texts) + R
