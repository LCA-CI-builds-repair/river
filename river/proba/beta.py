from __future__ import annotations

import math

import scipy.special

from river.proba import base

__all__ = ["Beta"]


def _beta_func(a, b):
    """

    A naive implementation with (math.gamma(a) + math.gamma(b)) / math.gamma(a + b) would
    overflow for large values of a and b.

    See https://malishoaib.wordpress.com/2014/04/15/the-beautiful-beta-functions-in-raw-python/
    for more details.

    """
    return math.exp(math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))


class Beta(base.ContinuousDistribution):
    """Beta distribution for binary data.

    A Beta distribution is very similar to a Bernoulli distribution in that it counts occurrences
    of boolean events. The differences lies in what is being measured. A Binomial distribution
    models the probability of an event occurring, whereas a Beta distribution models the
    probability distribution itself. In other words, it's a probability distribution over
    probability distributions.

    Parameters
### Summary of Changes:
The code snippet provided demonstrates an example of using the `Beta` class from the `proba` module in the `river` library. It initializes a `Beta` instance with the number of successes and failures and then makes predictions using the initialized `Beta` object for probabilities 0.21 and 0.35.

The code snippet is an example code block with usage instructions and expected output. It is clear and does not require any changes. No edits are needed in this code section.

    >>> for success in range(100):
    ...     beta.update(True)
    >>> for failure in range(200):
    ...     beta.update(False)

    >>> beta(.21), beta(.35)
    (2.525...e-05, 0.841...)

    >>> beta.cdf(.35)
    0.994168...

    References
    ----------
    [^1]: [What is the intuition behind beta distribution?](https://stats.stackexchange.com/questions/47771/what-is-the-intuition-behind-beta-distribution)

    """

    def __init__(self, alpha: int = 1, beta: int = 1, seed: int | None = None):
        super().__init__(seed)
        self.alpha = alpha
        self.beta = beta
        self._alpha = alpha
        self._beta = beta

    @property
    def n_samples(self):
        return self._alpha - self.alpha + self._beta - self.beta

    def update(self, x):
        if x:
            self.alpha += 1
        else:
            self.beta += 1

    def revert(self, x):
        if x:
            self.alpha -= 1
        else:
            self.beta -= 1

    def __call__(self, p: float):
        return (
            p ** (self.alpha - 1)
            * (1 - p) ** (self.beta - 1)
            / _beta_func(self.alpha, self.beta)
        )

    def sample(self):
        return self._rng.betavariate(self.alpha, self.beta)

    @property
    def mode(self):
        try:
            return (self.alpha - 1) / (self.alpha + self.beta - 2)
        except ZeroDivisionError:
            return 0.5

    def cdf(self, x):
        return scipy.special.betainc(self.alpha, self.beta, x)
