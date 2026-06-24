# ───────────────────────────────────────────────────────────────────────────
# src/runtime_ops.py
# Pure runtime helpers shared by the interpreter (only depend on numpy + errors,
# so they are unit-testable without the full sympy/scipy toolchain):
#   * check_power            — reject negative base ^ non-integer power
#   * index_key              — normalise an index value for a target container
#   * nested_setitem         — a[i][j] / a[i, j] assignment at any rank
#   * raise_binop_value_error— friendly Arabic message for numpy ValueErrors
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import numpy as np
from errors import HassoobRuntimeError, to_arabic_digits

# Arabic verbs for the element-wise operators, used in dimension-error messages.
_ELEMENTWISE_VERB = {"+": "جمع", "-": "طرح", "*": "ضرب"}


def check_power(base, exp) -> None:
    """امنع رفع عدد سالب إلى أُسٍّ غير صحيح (نتيجته عدد مركّب غير مدعوم).

    Raising a negative real number to a non-integer power yields a complex
    number, which the language does not support yet. Detect that case early and
    raise a friendly Arabic error instead of crashing (or silently producing a
    complex literal in the optimizer). Symbolic / array / boolean operands are
    left untouched so the caller can handle them normally.
    """
    if isinstance(base, bool) or isinstance(exp, bool):
        return
    if isinstance(base, (int, float)) and isinstance(exp, (int, float)):
        if base < 0:
            try:
                is_integer_power = float(exp).is_integer()
            except (ValueError, OverflowError):
                is_integer_power = False
            if not is_integer_power:
                raise HassoobRuntimeError(
                    "الأعداد العقدية غير مدعومة بعد، فلا يمكن رفع عددٍ سالبٍ "
                    "إلى أُسٍّ غير صحيح",
                    hint="استعمل أُسًّا صحيحًا مع الأعداد السالبة، أو اجعل الأساس موجبًا.",
                )


def index_key(target, index):
    """حوّل قيمة الفهرس إلى مفتاح مناسب للنوع الهدف.

    A tuple index (from the comma form a[i, j]) becomes a tuple of ints for
    numpy multi-indexing; a scalar index becomes a single int. Non-sequence
    targets keep the raw index (e.g. dict-like access).
    """
    if isinstance(target, (list, str, tuple, np.ndarray)):
        if isinstance(index, tuple):
            return tuple(int(i) for i in index)
        return int(index)
    return index


def nested_setitem(container, index_values, value):
    """أسند قيمة عبر سلسلة من مجموعات الفهارس.

    ``index_values`` has one entry per bracket group, e.g. a[i][j] -> [i, j]
    and a[i, j] -> [(i, j)]. We descend through all but the last group, then
    assign into the final container. Works for nested (ragged) lists and numpy
    arrays alike.
    """
    obj = container
    for key in index_values[:-1]:
        obj = obj[index_key(obj, key)]
    obj[index_key(obj, index_values[-1])] = value


def _shape_str(x):
    """وصف الأبعاد بالأرقام العربية (مثل ٣×٢)، أو None إن تعذّر."""
    if isinstance(x, np.ndarray):
        return "×".join(to_arabic_digits(d) for d in x.shape)
    if isinstance(x, (list, tuple)):
        return to_arabic_digits(len(x))
    return None


def raise_binop_value_error(op, left, right, exc):
    """ترجم ValueError (غالبًا تعارض أبعاد NumPy) إلى رسالة عربية لطيفة.

    Always raises HassoobRuntimeError; never returns. Called from the
    interpreter's _binop ValueError handler so dimension mismatches surface as
    clear messages instead of a raw numpy traceback.
    """
    ls, rs = _shape_str(left), _shape_str(right)
    if op in _ELEMENTWISE_VERB:
        verb = _ELEMENTWISE_VERB[op]
        if ls is not None and rs is not None:
            raise HassoobRuntimeError(
                f"لا يمكن {verb} مصفوفة {ls} مع مصفوفة {rs} — يجب أن تتطابق الأبعاد",
                hint="عمليات (+، -، *) على المصفوفات تتطلّب الأبعاد نفسها.",
            )
        raise HassoobRuntimeError(
            f"تعذّر {verb} هاتين القيمتين بسبب عدم تطابق الأبعاد",
            hint="تأكّد أنّ القيمتين متوافقتا الأبعاد.",
        )
    if op == "**":
        if ls is not None and rs is not None:
            raise HassoobRuntimeError(
                f"لا يمكن ضرب المصفوفة {ls} بالمصفوفة {rs} ضربًا مصفوفيًّا — الأبعاد غير متوافقة",
                hint="للضرب المصفوفي (**) يجب أن يساوي عددُ أعمدة الأولى عددَ صفوف الثانية.",
            )
        raise HassoobRuntimeError(
            "لا يمكن ضرب هاتين القيمتين ضربًا مصفوفيًّا — الأبعاد غير متوافقة",
            hint="للضرب المصفوفي (**) يجب أن تتوافق الأبعاد الداخلية.",
        )
    raise HassoobRuntimeError(
        f"عملية '{op}' غير صالحة على هاتين القيمتين",
        hint="تأكّد من أنواع القيمتين وتوافقهما مع هذه العملية.",
    )
