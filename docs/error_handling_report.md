# Report: Error-Handling Philosophy & Design in "Hassoob Arabi" (حاسوب عربي)

> A document explaining **why** and **how** we report errors, what we chose to
> treat as a **semantic / static** error versus a **runtime** error, and why we
> report an undefined variable **once per name per scope** while still
> **highlighting every occurrence** in the editor. Written for the evaluator
> and for future developers.

---

## 1) The pipeline

A program flows through these stages (see `src/interpreter/pipeline.py`):

```
source → (lex + parse) → semantic analysis → optimise → interpret
```

Every error shares one friendly, unified shape
(`src/errors/base.py: HassoobError.formatted`):

```
📝 Error on line 4, column 18: unexpected syntax near ‹+›
   ↪ did you mean ‹...›?        (spelling suggestion when available)
   💡 ...                       (guidance hint)
```

- Columns are stored 0-based internally and **displayed 1-based** to match what
  the user sees.
- Each error category has an emoji + Arabic label: 🔤 lexical, 📝 syntax,
  🔍 semantic, 📚 multiple errors, ⚠️ runtime errors.

---

## 2) How we report syntax errors: "collect-all" + "cross-phase recovery"

Instead of stopping at the first error, we have two error listeners
(`src/interpreter/parsing.py`):

- **`_RaisingErrorListener` (fail-fast):** raises the first error immediately.
  Used by `parse_expression` (a single expression) where "collect-all" makes no
  sense.
- **`_CollectingErrorListener` (collect-all):** gathers **all**
  syntax errors into one list using ANTLR's automatic recovery, so the use sees them all in a single run.

On top of that we add **cross-phase recovery:** any statement that
fails to build is replaced with an inert `ErrorNode` instead of dropping the whole program, so semantic analysis still runs on what *was* successfully built, and syntax + semantic errors are surfaced together in a `MultiError`. A broken program is **never optimised or executed** so we can't catch runtime errors.

Raw English ANTLR messages are translated into calm Arabic via
`_friendly_syntax_error` (detecting an unclosed bracket, the expected tokens, etc.).

---

## 3) What counts as a semantic (static) error, and why?

Semantic analysis (`src/semantic.py`) catches errors that can be **proven
without running** the program:

1. **Undefined name** (not a variable, function, or builtin), respecting hoisting within each scope (which allows recursion and forward references for functions).
2. **Wrong argument count** for a call to a function whose arity is known.
3. **Misplaced control flow:** `إرجع` (return) outside a function, and `توقف`/`استمر` (break/continue) outside a loop.
4. **Constant division-by-zero:** `٩ / ٠` and `أ / ٠` when the divisor is a constant expression that evaluates to zero.

### Why are `٩/٠` and `أ/٠` semantic (static) errors, not runtime errors?

(See `_check_const_zero_division` and `_const_eval`.)

- When the divisor is a **constant expression**, we know for certain — **without  running anything** — that this division can only ever fail. There is no input, branch, or state that makes `٩/٠` valid. It is **obvious** and does not need to wait for runtime to be caught.
- Reporting it statically lets us point at the exact line/column and **refuse to run a provably broken program**, instead of waiting for the division to actually execute (which might sit in a rare branch, or never run at all in some execution, so the error would hide). 
- **We only check constants.** Any divisor that contains a variable, a call, or any dynamic value is left **to runtime**; its value isn't known statically,
  and we must not reject a program that could be valid (e.g. a divisor that is only zero for some inputs). 
  **Strict rule: the static check has zero false positives.**

### "Folding" in the semantic phase (constant folding for the static check)

`_const_eval` folds only numeric constants (`+ - * / ÷ % ^` and unary signs) to determine the divisor. It deliberately treats booleans and symbolic constants (pi / e / infinity) as "non-constant" to avoid surprising static errors, and
any operation that raises during evaluation is treated as "non-constant" rather than crashing the analyser.

---

## 4) Undefined variable: one error per name + highlight every occurrence

**The decision:** we report each undefined name **once per scope**
(`src/semantic.py: _require_declared` plus the `_reported_undeclared` set that is reset on entering each function in `_function`).

**Why?** A single misspelling can recur dozens or thousands of times; so reporting every use would drown the user in thousands of errors that share **one root cause**. This mirrors "error-type poisoning" in real compilers to avoid a flood
of follow-on errors. Resetting at function boundaries ensures an error in one
function never silences a same-named error in another.

**But we don't lose the other occurrences:** `_require_declared` exports the offending name via `err.symbol`, which `ide/diagnostics.build` expands into an **underline span for every textual occurrence** of the name (outside strings
and comments, via `occurrences`). The editor then draws an underline beneath **every** occurrence (Tk tag `diag_undefined`; Qt wavy red underline via `setExtraSelections`), while the problem list stays a single line.

Bottom line: **one clear, non-overwhelming message in the list, and every > occurrence highlighted in the editor** for the user to find and fix. 
---

## 5) What is left to runtime?

The language is dynamically typed (just like Mathematica), so there is no static type checking. Errors
that cannot be proven statically without false positives are left to runtime,
including:
- type errors (adding a string to a number, calling a non-callable, …);
- **dynamic** division-by-zero (divisor is a variable/call);
- index-out-of-range and missing keys;
- exceeding call depth (infinite recursion) → a friendly Arabic message in the
  interpreter.

---

## 6) "Folding" in the optimisation phase (constant folding in the optimiser)

The optimiser (`src/optimizer.py`) is pure (AST → AST; it doesn't mutate nodes, it returns new ones) and iterates to a fixpoint. It applies:

- **Constant folding** (numeric and string) — with important guards:
  - It never folds an operation that raises (`ZeroDivisionError`/`OverflowError`/…);
    it keeps the node so the error happens in its proper phase. And because semantic analysis runs before optimisation, a **constant** division-by-zero has already been rejected, so it never reaches the optimiser.
  - It does not fold a power with a negative base and a non-integer exponent (a complex result) — that is left to runtime to raise an Arabic error via `check_power`.
- **Algebraic identities:** `x+0`, `x*1`, `x^1`, `x^0`, … and `x*0 → 0` **only**
  when the dropped operand is side-effect-free (so we never drop a call like `اطبع("hi") * ٠`).
- **Division is NOT simplified by an identity:** `0/x` is **not** folded to `0`, because `x` may be zero at runtime and must raise a division-by-zero error rather than be silently removed. The constant `c/0` is caught even earlier as
  a static semantic error.
- **Short-circuiting** (`و`/`أو`), **dead-code elimination** (impossible `إذا` branches, `بينما (خطأ)`), and **strength reduction** (`x^2 → x*x`, `x^3 → x*x*x` for side-effect-free operands).
- `_carry_pos` preserves the line/column on rebuilt nodes, so post-optimisation
  errors can still point at the original position.