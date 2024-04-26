from __future__ import annotations

import csv
import datetime as dt
import random

from .. import base
from . import utils

__all__ = ["iter_csv"]


class DictReader(csv.DictReader):
    """Overlay on top of `csv.DictReader` which allows sampling."""

    def __init__(self, fraction, rng, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fraction = fraction
        self.rng = rng

    def __next__(self):
import csv
import datetime as dt
import random
from csv import DictReader
from river import base, utils
from river.utils.typing import Stream

def iter_csv(
    filepath_or_buffer,
    target: str | list[str] | None = None,
    converters: dict | None = None,
    parse_dates: dict | None = None,
    drop: list[str] | None = None,
    drop_nones=False,
    fraction=1.0,
    compression="infer",
    seed: int | None = None,
    field_size_limit: int | None = None,
    **kwargs,
) -> Stream:
    """Iterates over rows from a CSV file.

    Reading CSV files can be quite slow. If, for whatever reason, you're going to loop through
    the same file multiple times, then we recommend that you to use the `stream.Cache` utility.

    Parameters
    ----------
    filepath_or_buffer
        Either a string indicating the location of a file, or a buffer object that has a
        `read` method.
    target
        A single target column is assumed if a string is passed. A multiple output scenario
        is assumed if a list of strings is passed. A `None` value will be assigned to each `y`
        if this parameter is omitted.
    converters
        All values in the CSV are interpreted as strings by default. You can use this parameter to
        cast values to the desired type. This should be a `dict` mapping feature names to callables
        used to parse their associated values. Note that a callable may be a type, such as `float`
        and `int`.
    ...
    csv.field_size_limit(limit)
