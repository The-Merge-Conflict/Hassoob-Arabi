# ---------------------------------------------------------------------------
# src/library/statistics.py
# Statistics built-ins (NumPy).
# ---------------------------------------------------------------------------
from __future__ import annotations

import random

import numpy as np

from ._shared import _as_number_list


def _b_mean(lst):   return float(np.mean(_as_number_list(lst)))


def _b_median(lst): return float(np.median(_as_number_list(lst)))


def _b_var(lst):    return float(np.var(_as_number_list(lst)))


def _b_std(lst):    return float(np.std(_as_number_list(lst)))


def _b_min(lst):    return min(_as_number_list(lst))


def _b_max(lst):    return max(_as_number_list(lst))


def _b_range(lst):
    data = _as_number_list(lst)
    return max(data) - min(data)


def _b_sum(lst):    return sum(_as_number_list(lst))


def _b_prod(lst):   return np.prod(_as_number_list(lst)).item()


def _b_corr(a, b):  return float(np.corrcoef(_as_number_list(a), _as_number_list(b))[0, 1])


def _b_random(n=None):
    if n is None:
        return random.random()
    return np.random.rand(int(n))


REGISTRY = {
    "متوسط": _b_mean,
    "وسيط": _b_median,
    "تباين": _b_var,
    "انحراف_معياري": _b_std,
    "أصغر": _b_min,
    "أكبر": _b_max,
    "مدى": _b_range,
    "مجموع": _b_sum,
    "ناتج": _b_prod,
    "ارتباط": _b_corr,
    "عشوائي": _b_random,
}
