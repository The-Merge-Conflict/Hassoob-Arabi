# ───────────────────────────────────────────────────────────────────────────
# src/repl.py
# Interactive REPL for حاسوب عربي.
#
# Uses prompt_toolkit when available (history, tab-completion, multi-line) and
# transparently falls back to a plain input() loop when it is not installed.
# ───────────────────────────────────────────────────────────────────────
from __future__ import annotations
import os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (os.path.join(_ROOT, "generated"), _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from errors import HassoobError
from interpreter import Interpreter, parse_program
from optimizer import optimize
from semantic import analyse
from _builtins_loader import BUILTINS, BUILTIN_NAMES, format_value, to_arabic_digits

PROMPT = "حاسوب عربي ← "
CONT_PROMPT = "            … "
HISTORY_PATH = os.path.expanduser("~/.hassoobarabi_history")

KEYWORDS = [
    "دالة", "إذا", "وإلا", "بينما", "لكل", "من", "إلى", "في", "بخطوة",
    "إرجع", "اوقف", "استمر", "صح", "خطأ", "فارغ", "رمز", "ليس", "و", "أو",
    "باي", "لانهاية",
]


def _is_incomplete(source: str) -> bool:
    """Heuristic: input is incomplete while braces/brackets/parens are unbalanced."""
    depth = 0
    in_string = None
    prev = ""
    for ch in source:
        if in_string:
            if ch == in_string and prev != "\\":
                in_string = None
        elif ch in "\"'":
            in_string = ch
        elif ch in "{[(":
            depth += 1
        elif ch in "}])":
            depth -= 1
        prev = ch
    return depth > 0 or in_string is not None


def _print_result(value):
    if value is None:
        return
    sympy = sys.modules.get("sympy")
    if sympy is not None and isinstance(value, sympy.Basic):
        print("←")
        # Pretty-print symbolic results, with Arabic numerals in the output.
        print(to_arabic_digits(sympy.pretty(value, use_unicode=True)))
    else:
        print(f"← {format_value(value)}")


def _print_help():
    print("دوال حاسوب عربي المدمجة:")
    names = sorted(BUILTIN_NAMES)
    width = 4
    for i in range(0, len(names), width):
        print("   " + "   ".join(names[i:i + width]))
    print("\nالأوامر الخاصة: مساعدة ، مسح ، خروج")


def _handle_command(text: str) -> bool:
    """Handle special non-language commands. Returns True if handled."""
    cmd = text.strip()
    if cmd in ("خروج", "exit", "quit"):
        raise SystemExit(0)
    if cmd in ("مساعدة", "help"):
        _print_help()
        return True
    if cmd in ("مسح", "clear"):
        os.system("cls" if os.name == "nt" else "clear")
        return True
    return False


def _run_one(interp: Interpreter, source: str):
    program = parse_program(source)
    program = optimize(program)
    analyse(program, builtin_names=list(BUILTINS.keys()))
    interp.run(program, interp.global_env)


# ── prompt_toolkit-backed loop ──────────────────────────────────────
def _run_prompt_toolkit(interp: Interpreter):
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.completion import WordCompleter

    completer = WordCompleter(sorted(set(BUILTIN_NAMES) | set(KEYWORDS)), sentence=True)
    session = PromptSession(history=FileHistory(HISTORY_PATH), completer=completer)

    while True:
        try:
            text = session.prompt(PROMPT)
            while _is_incomplete(text):
                text += "\n" + session.prompt(CONT_PROMPT)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        if not text.strip():
            continue
        if _handle_command(text):
            continue
        try:
            _run_one(interp, text)
            _print_result(interp.last_value)
        except HassoobError as err:
            print(err.formatted())
        except SystemExit:
            raise
        except Exception as err:  # pragma: no cover - defensive, keep REPL alive
            print(f"🌸 عذرًا، حدث خطأ غير متوقّع: {err}")


# ── plain fallback loop ─────────────────────────────────────────
def _run_plain(interp: Interpreter):
    while True:
        try:
            text = input(PROMPT)
            while _is_incomplete(text):
                text += "\n" + input(CONT_PROMPT)
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            break
        if not text.strip():
            continue
        if _handle_command(text):
            continue
        try:
            _run_one(interp, text)
            _print_result(interp.last_value)
        except HassoobError as err:
            print(err.formatted())
        except SystemExit:
            raise
        except Exception as err:  # pragma: no cover
            print(f"🌸 عذرًا، حدث خطأ غير متوقّع: {err}")


def start_repl():
    """بدء حلقة التفاعل / launch the interactive REPL."""
    interp = Interpreter(repl_mode=False)  # we print results ourselves, prettily
    print("مرحبًا بك في حاسوب عربي! اكتب 'مساعدة' للأوامر أو 'خروج' للإنهاء.")
    try:
        _run_prompt_toolkit(interp)
    except ImportError:
        _run_plain(interp)


if __name__ == "__main__":
    start_repl()
