from __future__ import annotations

import functools

from river.stats import Var

from ..utils import BranchFactory
from .base import Splitter


class EBSTSplitter(Splitter):
    """iSOUP-Tree's Extended Binary Search Tree (E-BST).

    This class implements the Extended Binary Search Tree[^1] (E-BST)
    structure, using the variant employed by Osojnik et al.[^2] in the
    iSOUP-Tree algorithm. This structure is employed to observe the target
    space distribution.

    Proposed along with Fast Incremental Model Tree with Drift Detection[^1] (FIMT-DD), E-BST was
    the first attribute observer (AO) proposed for incremental Hoeffding Tree regressors. This
    AO works by storing all observations between splits in an extended binary search tree
    structure. E-BST stores the input feature realizations and statistics of the target(s) that
    enable calculating the split heuristic at any time. To alleviate time and memory costs, E-BST
    implements a memory management routine, where the worst split candidates are pruned from the
    binary tree.

    In this variant, only the left branch statistics are stored and the complete split-enabling
import collections
import functools
from river import base, stats

class EBSTNode:
    def __init__(self, att_val, target_val, w):
        self.att_val = att_val

        if isinstance(target_val, dict):
            # Import VectorDict here to prevent circular import of river.utils
            from river.utils import VectorDict

            self.estimator = VectorDict(default_factory=functools.partial(Var))
            self._update_estimator = self._update_estimator_multivariate
        else:
            self.estimator = Var()
            self._update_estimator = self._update_estimator_univariate

        self._update_estimator(self, target_val, w)

        self._left = None
        self._right = None

    @staticmethod
    def _update_estimator_univariate(node, target, w):
        node.estimator.update(target, w)

    @staticmethod
    def _update_estimator_multivariate(node, target, w):
        for t in target:
            node.estimator[t].update(target[t], w)

    # Incremental implementation of the insert method. Avoiding unnecessary
    # stack tracing must decrease memory costs
    def insert_value(self, att_val, target_val, w):
        current = self
        antecedent = None
        is_right = False

        while current is not None:
            antecedent = current
            if att_val == current.att_val:
                self._update_estimator(current, target_val, w)
                return
            elif att_val < current.att_val:
                self._update_estimator(current, target_val, w)

                current = current._left
                is_right = False
            else:
                current = current._right
                is_right = True

        # Value was not yet added to the tree
        if is_right:
            antecedent._right = EBSTNode(att_val, target_val, w)
        else:
            antecedent._left = EBSTNode(att_val, target_val, w)
