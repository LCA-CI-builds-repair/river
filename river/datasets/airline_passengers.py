from __future__ import annotations

from river import stream

from . import base


class AirlinePassengers(base.FileDataset):
    """Monthly number of international airline passengers.

    The stream contains 144 items and only one single feature, which is the month. The goal is to
    predict the number of passengers each month by capturing the trend and the seasonality of the
    data.
"""Airline Passengers dataset.

This is a time series dataset collected by OECD (Organisation for Economic Co-operation and Development)
for the period of January 1949 to December 1960. The dataset contains the number of airline passengers
passed monthly, with the first entry being the total number of passengers.

References
----------
[^1]: OECD. (1961). International Air Transport Statistics: August 1960. OECD Publishing.
[^2]: Smith, D. J., & Bivand, O. A. (1993). Time series analysis and its application in finance. John Wiley & Sons.

"""

    def __init__(self):
        super().__init__(
            filename="airline-passengers.csv",
            task=base.REG,
            n_features=1,
            n_samples=144,
        )

    def __iter__(self):
        return stream.iter_csv(
            self.path,
            target="passengers",
            converters={"passengers": int},
            parse_dates={"month": "%Y-%m"},
        )
