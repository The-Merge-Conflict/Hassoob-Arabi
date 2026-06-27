#!/usr/bin/env python3
# ───────────────────────────────────────────────────────────────────────────
# main.py — entry point for حاسوب عربي.
#
# Usage:
#   python main.py                  # start the interactive REPL
#   python main.py script.حع        # execute a script file
#   python main.py -c "اطبع(٣+٤)"   # execute a single expression / program string
# ───────────────────────────────────────────────────────────────────────
from __future__ import annotations
import os, sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_ROOT, "generated"), os.path.join(_ROOT, "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from errors import HassoobError
from interpreter import Interpreter, compile_program


def run_program_source(source: str, repl_mode: bool = False) -> int:
    """Run a full program string through the whole pipeline."""
    interp = Interpreter(repl_mode=repl_mode)
    try:
        program = compile_program(source)
        interp.run(program, interp.global_env)
        return 0
    except HassoobError as err:
        print(err.formatted(), file=sys.stderr)
        return 1


def _usage() -> str:
    return (
        "الاستخدام:\n"
        "  python main.py                 # بدء الوضع التفاعلي (REPL)\n"
        "  python main.py ملف.حع        # تنفيذ ملف برنامج\n"
        '  python main.py -c "اطبع(٣+٤)" # تنفيذ نص مباشرة\n'
        "  python main.py --ide          # فتح بيئة التطوير الرسومية (RTL)\n"
    )


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    # --ide / -g → launch the graphical IDE.
    if argv and argv[0] in ("--ide", "-g", "--gui"):
        from ide import launch
        return launch() or 0

    # No arguments → interactive REPL.
    if not argv:
        from repl import start_repl
        try:
            start_repl()
        except SystemExit:
            pass
        return 0

    # -c "..." → execute a string.
    if argv[0] in ("-c", "--command"):
        if len(argv) < 2:
            print(_usage(), file=sys.stderr)
            return 2
        return run_program_source(argv[1], repl_mode=True)

    if argv[0] in ("-h", "--help"):
        print(_usage())
        return 0

    # Otherwise treat the first argument as a script path.
    path = argv[0]
    if not os.path.isfile(path):
        print(f"خطأ: الملف ‹{path}› غير موجود", file=sys.stderr)
        return 1
    with open(path, "r", encoding="utf-8") as fh:
        source = fh.read()
    return run_program_source(source, repl_mode=False)


if __name__ == "__main__":
    sys.exit(main())
