# ───────────────────────────────────────────────────────────────────────────
# tests/test_ide.py
# Headless tests for the IDE's Tkinter-free building blocks: the syntax
# highlighter and the execution engine.  (No tkinter import here.)
# ───────────────────────────────────────────────────────────────────────────
import os
import sys

# Force matplotlib headless before anything imports builtins (engine -> builtins).
os.environ.setdefault("HASSOOB_HEADLESS", "1")

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (_ROOT, os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# register the phase folders (frontend/midend/backend/driver) on sys.path
import _pathsetup  # noqa: F401,E402

from ide.highlight import Highlighter, Span  # noqa: E402
from ide.engine import HassoobEngine, RunResult  # noqa: E402

_passed = 0
_failed = 0


def check(cond, label):
    global _passed, _failed
    if cond:
        _passed += 1
    else:
        _failed += 1
        print(f"  ✖ {label}")


def _tags_for(text, hl):
    return {(s.tag, text[s.start:s.end]) for s in hl.spans(text)}


def test_highlighter_basics():
    hl = Highlighter(["اطبع", "جذر"])
    code = 'ملاحظة تعليق\nإذا صح:\n    اطبع("مرحبا")\nس = ١٢٣ + 4'
    spans = hl.spans(code)
    tags = {s.tag for s in spans}
    check("comment" in tags, "comment detected")
    check("keyword" in tags, "keyword detected")
    check("constant" in tags, "constant detected")
    check("builtin" in tags, "builtin detected")
    check("string" in tags, "string detected")
    check("number" in tags, "number detected")
    pairs = _tags_for(code, hl)
    check(("builtin", "اطبع") in pairs, "اطبع is a builtin span")
    check(("keyword", "إذا") in pairs, "إذا is a keyword span")
    check(("number", "١٢٣") in pairs, "arabic-indic number span")
    check(("number", "4") in pairs, "western number span")
    # spans must be ordered and non-overlapping
    ordered = all(
        spans[i].end <= spans[i + 1].start for i in range(len(spans) - 1)
    )
    check(ordered, "spans are ordered & non-overlapping")


def test_highlighter_no_builtins():
    hl = Highlighter([])
    spans = hl.spans("دالة ف(س): إرجع س")
    check(any(s.tag == "keyword" for s in spans), "keywords work without builtins")


def test_engine_construction():
    eng = HassoobEngine()
    check(len(eng.builtin_names) > 0, "engine exposes builtin names")
    check("اطبع" in eng.builtin_names, "اطبع is a known builtin")


def test_engine_runresult_shape():
    eng = HassoobEngine()
    res = eng.run_source('اطبع("مرحبا")')
    check(isinstance(res, RunResult), "run_source returns RunResult")
    # Without the generated ANTLR parser we expect a friendly, non-crashing
    # error rather than an exception.
    if res.error is not None:
        check(not res.ok, "missing-parser path reports not-ok")
        check("🔧" in res.error or "🌸" in res.error or "⚠" in res.error,
              "error message is cute/friendly Arabic")
    else:
        # Parser present: program should have produced output.
        check(res.ok, "successful run is ok")


def test_engine_handles_blank():
    eng = HassoobEngine()
    res = eng.eval_line("")
    check(isinstance(res, RunResult), "eval_line returns RunResult for blank input")


def run():
    print("tests/test_ide.py")
    for fn in (
        test_highlighter_basics,
        test_highlighter_no_builtins,
        test_engine_construction,
        test_engine_runresult_shape,
        test_engine_handles_blank,
    ):
        fn()
    total = _passed + _failed
    print(f"{_passed}/{total} passed")
    return _failed == 0


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
