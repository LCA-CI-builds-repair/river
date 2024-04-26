"""Utilities for unit testing and sanity checking estimators."""
from __future__ import annotations

import functools
import typing

import numpy as np

from river.base import Estimator
from river.model_selection.base import ModelSelector
from river.reco.base import Ranker

from . import anomaly, clf, common, model_selection, reco

__all__ = ["check_estimator", "yield_checks"]


def _allow_exception(func, exception):
    def f(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except exception:
            pass

    f.__name__ = func.__name__
    return f


def _wrapped_partial(func, *args, **kwargs):
    """

    Taken from http://louistiao.me/posts/adding-__name__-and-__doc__-attributes-to-functoolspartial-objects/

    """
    partial = functools.partial(func, *args, **kwargs)
    functools.update_wrapper(partial, func)
    return partial


class _DummyDataset:
    def __init__(self, *data):
        self.data = data

    def __iter__(self):
        yield from self.data


def _yield_datasets(model: Estimator):
    """Generates datasets for a given model."""

    from sklearn import datasets as sk_datasets
import numpy as np
import typing
from river import base, compose, datasets, preprocessing, stream, utils
from river.utils.typing import Estimator
from river.utils import inspect
from river.utils.testing import common
from sklearn import datasets as sk_datasets

def yield_checks(model: Estimator) -> typing.Iterator[typing.Callable]:
    """Generates unit tests for a given model.

    Parameters
    ----------
    model

    """

    from river import base, utils

    # General checks
    yield common.check_repr
    yield common.check_str
    yield common.check_tags
    yield common.check_clone_same_class
    yield common.check_clone_is_idempotent
    yield common.check_init_has_default_params_for_tests
    yield common.check_init_default_params_are_not_mutable
    yield common.check_doc
    yield common.check_clone_changes_memory_addresses
    yield common.check_mutate_can_be_idempotent
    if model._mutable_attributes:
        yield common.check_mutable_attributes_exist

    if isinstance(model, base.Wrapper):
        yield common.check_wrapper_accepts_kwargs

    # Checks that make use of datasets
    dataset_checks = [
        common.check_learn_one,
        common.check_pickling,
        common.check_shuffle_features_no_impact,
        common.check_emerging_features,
        common.check_disappearing_features,
    ]

    if hasattr(model, "debug_one"):
        dataset_checks.append(common.check_debug_one)

    if model._is_stochastic:
        dataset_checks.append(common.check_seeding_is_idempotent)

    # Classifier checks
    if utils.inspect.isclassifier(model) and not utils.inspect.ismoclassifier(model):
        dataset_checks.append(_allow_exception(clf.check_predict_proba_one, NotImplementedError))
        # Specific checks for binary classifiers
        if not model._multiclass:  # type: ignore
            dataset_checks.append(
                _allow_exception(clf.check_predict_proba_one_binary, NotImplementedError)
            )

    if isinstance(utils.inspect.extract_relevant(model), ModelSelector):
        dataset_checks.append(model_selection.check_model_selection_order_does_not_matter)

    if isinstance(utils.inspect.extract_relevant(model), Ranker):
        yield reco.check_reco_routine

    if utils.inspect.isanomalydetector(model):
from river import base, utils
from river.utils.testing import common

# General checks
yield common.check_repr
yield common.check_str
yield common.check_tags
yield common.check_clone_same_class
yield common.check_clone_is_idempotent
yield common.check_init_has_default_params_for_tests
yield common.check_init_default_params_are_not_mutable
yield common.check_doc
yield common.check_clone_changes_memory_addresses
yield common.check_mutate_can_be_idempotent
if model._mutable_attributes:

    """
    for check in yield_checks(model):
        if check.__name__ in model._unit_test_skips():
            continue
        check(model.clone())
