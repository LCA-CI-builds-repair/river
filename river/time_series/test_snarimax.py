from __future__ import annotations

import calendar
import math
import random

import pytest
import sympy

from river import compose, datasets, metrics, time_series
from river.time_series.snarimax import Differencer


class Yt(sympy.IndexedBase):
    t = sympy.symbols("t", cls=sympy.Idx)

    def __getitem__(self, idx):
        return super().__getitem__(self.t - idx)


def test_diff_formula():
    """

    >>> import sympy
    >>> from river.time_series.snarimax import Differencer

    >>> Y = Yt('y')
    >>> Y
    y

    >>> p = sympy.symbols('p')
    >>> p
    p

    >>> D = Differencer

    1
    >>> D(0).diff(p, Y)
    p

    (1 - B)
    >>> D(1).diff(p, Y)
    p - y[t]

    (1 - B)^2
    >>> D(2).diff(p, Y)
    p + y[t - 1] - 2*y[t]

    (1 - B^m)
    >>> m = sympy.symbols('m', cls=sympy.Idx)
    >>> D(1, m).diff(p, Y)
    p - y[-m + t + 1]

    (1 - B)(1 - B^m)
    >>> (D(1) * D(1, m)).diff(p, Y)
    p - y[-m + t + 1] + y[-m + t] - y[t]

    (1 - B)(1 - B^12)
    >>> (D(1) * D(1, 12)).diff(p, Y)
    p - y[t - 11] + y[t - 12] - y[t]

    """
import pytest
import random
import math
import pandas as pd
import calendar

from river.time_series.snarimax import Differencer
from river import time_series, compose, datasets, metrics

def test_diff_example():
    """
    https://people.duke.edu/~rnau/411sdif.htm

    >>> import pandas as pd
    >>> from river.time_series.snarimax import Differencer

    >>> sales = pd.DataFrame([
    ...     {'date': 'Jan-70', 'autosale': 4.79, 'cpi': 0.297},
    ...     {'date': 'Feb-70', 'autosale': 4.96, 'cpi': 0.298},
    ...
    ])

    >>> sales['autosale/cpi'] = sales.eval('autosale / cpi').round(2)
    >>> Y = sales['autosale/cpi'].to_list()

    >>> diff = Differencer(1)
    >>> sales['(1 - B)'] = [
    ...     diff.diff(p, Y[:i][::-1])
    ...     if i else ''
    ...
    ]

    >>> sdiff = Differencer(1, 12)
    >>> sales['(1 - B^12)'] = [
    ...     sdiff.diff(p, Y[:i][::-1])
    ...     if i >= 12 else ''
    ...
    ]

    >>> sales['(1 - B)(1 - B^12)'] = [
    ...     (diff * sdiff).diff(p, Y[:i][::-1])
    ...     if i >= 13 else ''
    ...
    ]

    >>> sales
    ...

    """

@pytest.mark.parametrize(
    "differencer",
    [
        Differencer(1),
        Differencer(2),
        ...
    ],
)
def test_undiff(differencer):
    ...

@pytest.mark.parametrize(
    "snarimax, Y, errors, expected",
    [
        ...
    ],
)
def test_add_lag_features(snarimax, Y, errors, expected):
    ...

@pytest.mark.parametrize(
    "snarimax",
    [
        ...
    ],
)
def test_no_overflow(snarimax):
    ...
