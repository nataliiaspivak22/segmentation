"""
Tools helping to make code neat
"""
from typing import Union


def short_format(value: Union[int, float]) -> Union[str, float]:
    """
    Returns input value in a format 1000 --> 1K
    :param value: input value
    :return: string
    """
    short_value = value
    if (short_value > 1000):
        magnitude = 0
        while abs(short_value) >= 1:
            magnitude += 1
            short_value /= 1000
        # add more suffixes if you need them
        short_value = '%.2f%s' % (short_value, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    return short_value