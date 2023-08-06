"""
 * @param {number} n
 * @param {number} hu
 * @param {number} a
 * @param {number} li
 * @returns {number}
"""


def hf(n, hu, a, li):
    k = (n + hu / 30) % 12
    return li - a * max(min(k - 3, 9 - k, 1), -1)
