"""
Only include python-generic stuff in here.

Django-specific stuff goes in db.py, template.py, etc.
"""
from decimal import Decimal
from itertools import izip


def find_key(dct, val):
    """
    Return the key of dictionary for value.
    If multiple matches, only one is returned.
    None for no matches.
    """
    return dict(izip(dct.values(), dct.keys())).get(val, None)


def make_decimal(amount, places=2):
    "Convenience function to create/convert to a decimal with n dec places"
    return Decimal(amount).quantize(Decimal(10) ** -places)
