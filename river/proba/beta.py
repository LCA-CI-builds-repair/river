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
    ----------
    alpha
        Initial alpha parameter.
    beta
        Initial beta parameter.
    seed
        Random number generator seed for reproducibility.

    Examples
    --------

    >>> from river import proba

    >>> successes = 81
    >>> failures = 219
    >>> beta = proba.Beta(successes, failures)

    >>> beta(.21), beta(.35)
import scipy.stats as stats

beta = stats.beta(1, 1)

for success in range(100):
    beta = beta.rvs()
for failure in range(200):
    beta = beta.rvs()

beta_rvs_21 = beta.rvs(0.21)
beta_rvs_35 = beta.rvs(0.35)

beta_cdf_35 = beta.cdf(0.35)

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
        return self

    def revert(self, x):
        if x:
            self.alpha -= 1
        else:
            self.beta -= 1
        return self

    def __call__(self, p: float):
        return (
            p ** (self.alpha - 1) * (1 - p) ** (self.beta - 1) / _beta_func(self.alpha, self.beta)
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
