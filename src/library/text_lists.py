# ---------------------------------------------------------------------------
# src/library/text_lists.py
# List / string / type built-ins.
# ---------------------------------------------------------------------------
from __future__ import annotations

import sys

import numpy as np

from errors import HassoobRuntimeError
from ._shared import _to_int_index


def _b_len(x):
    try:
        return len(x)
    except TypeError:
        raise HassoobRuntimeError("لا يمكن حساب طول هذا النوع")


def _b_slice(s, start, end):
    return s[_to_int_index(start):_to_int_index(end)]


def _b_replace(s, old, new):
    return str(s).replace(str(old), str(new))


def _b_split(s, sep):
    return str(s).split(str(sep))


def _b_join(sep, lst):
    return str(sep).join(str(x) for x in lst)


def _b_type_name(x):
    sympy_mod = sys.modules.get("sympy")
    if x is None:
        return "فارغ"
    if isinstance(x, bool):
        return "منطقي"
    if isinstance(x, (int, float)):
        return "عدد"
    if isinstance(x, str):
        return "نص"
    if isinstance(x, np.ndarray):
        return "مصفوفة"
    if sympy_mod is not None and isinstance(x, sympy_mod.Basic):
        return "رمزي"
    if isinstance(x, (list, tuple)):
        return "قائمة"
    if callable(x):
        return "دالة"
    return "غير معروف"


def _b_list_from(start, end, step=1):
    return list(range(_to_int_index(start), _to_int_index(end) + 1, _to_int_index(step)))


def _b_sort(lst, عكسي=False):
    return sorted(list(lst), reverse=bool(عكسي))


def _b_reverse(lst_or_str):
    if isinstance(lst_or_str, str):
        return lst_or_str[::-1]
    return list(reversed(list(lst_or_str)))


def _b_map(fn, lst):
    if not callable(fn):
        raise HassoobRuntimeError("الوسيط الأول لـ طبّق يجب أن يكون دالة")
    return [fn(x) for x in lst]


def _b_filter(fn, lst):
    if not callable(fn):
        raise HassoobRuntimeError("الوسيط الأول لـ صفّي يجب أن يكون دالة")
    return [x for x in lst if fn(x)]


REGISTRY = {
    "طول": _b_len,
    "قطعة": _b_slice,
    "استبدل": _b_replace,
    "قسم": _b_split,
    "دمج": _b_join,
    "نوع": _b_type_name,
    "قائمة_من": _b_list_from,
    "ترتيب": _b_sort,
    "عكس": _b_reverse,
    "طبق": _b_map,
    "صفي": _b_filter,
    "اختر": _b_filter,   # اختر is an alias of صفّي
}
