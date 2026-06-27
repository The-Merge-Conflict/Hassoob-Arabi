# حاسوب عربي (Hassoob Arabi)

> An **Arabic-first programming language** and its compiler/interpreter, inspired by Wolfram Mathematica: fully Arabic syntax, a symbolic + numeric math engine, plotting, friendly Arabic error messages, and a right-to-left (RTL) IDE.
>
> لغة برمجة عربية بالكامل ومترجمها/مفسرها، مستوحاة من Wolfram Mathematica: بنية لغوية عربية، محرك رياضي رمزي وعددي، رسوم بيانية، رسائل أخطاء عربية لطيفة، وبيئة تطوير يمينية (RTL).

**Team / الفريق:** Jaafer Mahfoud · Laila Al-Abdullah · Hatem Ibrahim
**Repository:** https://github.com/The-Merge-Conflict/Hassoob-Arabi

📖 Full documentation: [`HassoobArabi_Documentation_EN.md`](HassoobArabi_Documentation_EN.md) · التوثيق الكامل بالعربية: [`HassoobArabi_Documentation_AR.md`](HassoobArabi_Documentation_AR.md)

---

## Table of Contents
1. [Overview](#1-overview)
2. [Modular Refactor](#2-modular-refactor)
3. [Architecture & Compilation Pipeline](#3-architecture--compilation-pipeline)
4. [Project Structure](#4-project-structure)
5. [Installation & Running](#5-installation--running)
6. [Language Reference](#6-language-reference)
7. [Built-in Function Catalog](#7-built-in-function-catalog)
8. [Error Handling](#8-error-handling)
9. [Example Programs](#9-example-programs)
10. [Tests](#10-tests)
11. [Future Work](#11-future-work)
12. [Repository & Team](#12-repository--team)

> **The documentation contains two guides:** a *Developer Guide* (extending the language, after section 4) and a *User Guide* (sections 5–7: running from scratch, and every command and task). Section 8 explains the error-handling philosophy, and section 6.10 covers normalization.

---

## 1. Overview

**Hassoob Arabi** (حاسوب عربي, *"Arabic Computer"*) is a complete programming language whose **keywords, identifiers, numerals, and error messages are all in Arabic**, and whose source files use the `.حع` extension. It is inspired by Wolfram Mathematica: beyond ordinary imperative programming, it treats **symbolic mathematics** as a first-class citizen — you can declare symbols, differentiate, integrate, take limits, expand Taylor series, solve equations, work with matrices, compute statistics, and draw plots, all using Arabic commands.

Key characteristics:

- **Arabic syntax** — control-flow keywords (`إذا`, `بينما`, `لكل`, `دالة`, …), built-in functions (`اطبع`, `اشتق`, `متوسط`, …), and operators read naturally in Arabic.
- **Arabic-Indic numerals** — both `٠١٢٣` and `0123` are accepted in source, and **all output is printed with Arabic numerals** (٠–٩).
- **Symbolic + numeric engine** — symbolic algebra/calculus via SymPy, fast numeric/linear-algebra via NumPy, plotting via Matplotlib.
- **Friendly errors** — every error is a cute, fully-Arabic message in the canonical form `خطأ في السطر {line}، العمود {col}: …`, often with a *"did you mean…"* (`هل تقصد`) suggestion.
- **RTL IDE** — a right-to-left editor with syntax highlighting, instant run, and an interactive REPL.

---

## 2. Modular Refactor

The four largest source files were split into **focused sub-packages** to improve abstraction and readability. Each package exposes an `__init__.py` that **re-exports the full public surface**, so every existing import (`from errors import …`, `from ast_nodes import …`, `from interpreter import …`) keeps working unchanged — **no call sites and no tests were modified**, and there is **no behavior change**.

| Before (single file) | After (package) | Sub-modules |
|---|---|---|
| `src/errors.py` | `src/errors/` | `base` (helpers + `HassoobError`), `syntax` (`LexError`, `ParseError`), `semantic` (`SemanticError`, `MultiError`), `runtime` (`HassoobRuntimeError`), `signals` (`ReturnSignal`/`BreakSignal`/`ContinueSignal`) |
| `src/ast_nodes.py` | `src/ast_nodes/` | `base` (`_Positioned` mix-in), `statements`, `expressions`, `literals` |
| `src/interpreter.py` | `src/interpreter/` | `evaluator` (`Function` value + `Interpreter`), `parsing` (ANTLR front-end, tashkeel stripping, friendly Arabic syntax errors, `parse_program`/`parse_expression`), `pipeline` (`run_source`) |
| `src/builtins.py` | `src/library/` | `formatting`, `symbolic`, `numeric`, `statistics`, `text_lists`, `plotting`, plus `_shared` helpers; `_builtins_loader.py` assembles the `BUILTINS` registry from these domains |

**Why it helps:** errors are now grouped by *kind* (lexer/parser vs. semantic vs. runtime), control-flow signals are cleanly separated from real errors, AST nodes are organized by category, the interpreter's parsing front-end is isolated from evaluation, and the standard library is split by mathematical domain.

### Physical split by compilation phase

In addition, the code is now organised physically into folders by compilation phase, to make the **front end, middle end, and back end** clearly visible:

- `src/frontend/` — Front End: normalization, lexing/parsing, and AST construction (`parsing`, `lang_utils`, `ast_nodes/`).
- `src/midend/` — Middle End: semantic analysis and optimisation (`semantic`, `optimizer`).
- `src/backend/` — Back End: execution, runtime, and the standard library (`evaluator`, `environment`, `runtime_ops`, `library/`, `_builtins_loader`).
- `src/driver/` — the Driver that wires the phases together (`pipeline`, `repl`), plus the shared `errors/` and the `interpreter/` package as a stable export façade.

`src/_pathsetup.py` registers these folders on the import path, so every import and every call site stays the same **with no behavioural change**. `src/ast_builder.py` (the provided file) stays in place under `src/` to honour its fixed layout.

---

## 3. Architecture & Translation Pipeline

Hassoob Arabi is a **tree-walking interpreter** built on an ANTLR4 front end. The code is now **organised physically by compilation phase** so the three layers are clearly visible: the front end in `src/frontend/`, the middle end in `src/midend/`, and the back end in `src/backend/`, wired together by a small driver in `src/driver/`, with the error hierarchy shared in `src/errors/`.

A source file flows through these phases:

```
  source.حع
      │
      ▼
┌────────────────────┐  Front End (src/frontend/)
│  lex / parse        │  ANTLR parser from HassoobArabi.g4 + normalization → parse tree → AST
└────────────────────┘
      │  AST
      ▼
┌────────────────────┐  Middle End (src/midend/)
│  semantic analysis  │  semantic.py: undefined names, arg counts, placement of return/break/continue
│  → then optimise    │  optimizer.py: constant folding, simplification, dead-branch removal
└────────────────────┘
      │  checked & optimised AST
      ▼
┌────────────────────┐  Back End (src/backend/)
│  interpret          │  evaluator.py walks the AST; environment.py for scopes; library/ for builtins
└────────────────────┘
      │
      ▼
  terminal output (Arabic numerals) + Matplotlib plot windows
```

The whole path is wired by `src/driver/pipeline.py` (`compile_program` then `run_source`, and `main.py`): **parse → analyse → optimise → interpret**. We always run semantic analysis **before** optimisation, so only a semantically valid program is ever optimised.

**The three layers and their responsibilities**

| Layer | Folder | Modules | Responsibility |
|---|---|---|---|
| Front End | `src/frontend/` (+ provided `src/ast_builder.py`) | `parsing`, `lang_utils`, `ast_nodes/`, `ast_builder` | Normalization, ANTLR lexing/parsing, translating ANTLR errors into friendly Arabic, and building the AST. |
| Middle End | `src/midend/` | `semantic`, `optimizer` | Static checks that collect all errors, then meaning-preserving optimisation. |
| Back End | `src/backend/` | `evaluator`, `environment`, `runtime_ops`, `library/`, `_builtins_loader` | Executing the AST, managing the scope chain (Mathematica-style), and the standard library. |
| Driver & shared | `src/driver/` + `src/errors/` + `src/interpreter/` | `pipeline`, `repl`, `errors`, `interpreter` (façade) | Wiring the phases into one path, the interactive shell, the error hierarchy, and a stable export façade. |
| Tooling | `ide/` | `engine`, `highlight`, `editor_qt`, `editor` | An RTL development environment with structural highlighting and instant run. |

> **Why split by phase?** It puts each responsibility in its natural place: to change the grammar or normalization look in the front end, to add an error check or simplification look in the middle end, and to change execution semantics look in the back end. `src/_pathsetup.py` registers these folders on the import path so modules keep importing each other by short name, with no behavioural change.

---

## 4. Project Structure

```
HassoobArabi/
├─ HassoobArabi.g4         ANTLR4 grammar (the language definition)
├─ generated/             ANTLR4-generated lexer/parser (build artifact)
├─ main.py                entry point (run file / REPL / -c / --ide)
├─ conftest.py            pytest path bootstrap (registers the phase folders)
├─ requirements.txt       Python dependencies
├─ src/
│  ├─ _pathsetup.py       registers the source root + every phase folder on sys.path
│  ├─ frontend/           Front End — lexing/parsing → AST
│  │  ├─ parsing.py         ANTLR front end + normalization + friendly Arabic syntax errors
│  │  ├─ lang_utils.py      shared lexing helpers (escapes, f-strings, comparison chaining)
│  │  └─ ast_nodes/         AST node classes (base, statements, expressions, literals)
│  ├─ ast_builder.py      (PROVIDED — unmodified) parse tree → AST; stays at src/ for its fixed layout
│  ├─ midend/             Middle End — semantic analysis + optimisation
│  │  ├─ semantic.py        static analysis that collects ALL errors (no stop-at-first)
│  │  └─ optimizer.py       AST optimiser (constant folding, simplification, dead-branch removal)
│  ├─ backend/            Back End — execution + runtime
│  │  ├─ evaluator.py       Function value + the Interpreter class
│  │  ├─ environment.py     scope chain
│  │  ├─ runtime_ops.py     operator / indexing runtime helpers
│  │  ├─ _builtins_loader.py loads BUILTINS from library/
│  │  └─ library/           standard library (formatting, symbolic, numeric, statistics, text_lists, plotting, _shared)
│  ├─ driver/             Driver — wires the phases together
│  │  ├─ pipeline.py        compile_program / run_source: parse → analyse → optimise → interpret
│  │  └─ repl.py            interactive shell
│  ├─ errors/             shared Arabic error hierarchy + control signals (base, syntax, semantic, runtime, signals)
│  └─ interpreter/        thin re-export façade that keeps the public import name stable
├─ ide/                   UI-agnostic engine + RTL editors (Qt primary, Tkinter fallback)
├─ tests/                 test suites (build ASTs directly)
└─ examples/              example programs (.حع)
```

---

## Developer Guide — Extending the Language

> This section is for **developers** who want to extend the language. Running the program from scratch and the explanation of every command and task live in the **User Guide** (sections 5, 6, and 7).

Because the code is organised physically by **compilation phase**, every kind of addition has a clear home:

### Adding a keyword or new syntax
1. Edit the grammar in `HassoobArabi.g4`, then regenerate the parser:
   `antlr4 -Dlanguage=Python3 -visitor -o generated HassoobArabi.g4`.
2. Add an appropriate AST node in `src/frontend/ast_nodes/` (in `statements.py`, `expressions.py`, or `literals.py`) and export it from `ast_nodes/__init__.py`.
3. Translate the parse tree into that node in `src/ast_builder.py` (provided; if a change is needed, this is the place).
4. Add static checks in `src/midend/semantic.py` (scope/argument checks), and if it can be simplified add a rule in `src/midend/optimizer.py`.
5. Implement execution semantics in `src/backend/evaluator.py`.

### Adding a new builtin
Add the function to the right domain in `src/backend/library/` (e.g. `numeric.py`, `symbolic.py`, `statistics.py`) and register it in that domain's registry; `_builtins_loader.py` gathers them automatically into `BUILTINS`. No grammar change is needed because calls are generic.

### Adding an error type
Use the hierarchy in `src/errors/` (`syntax`, `semantic`, or `runtime`); they all inherit from `HassoobError` and print in the same unified Arabic format, with optional *“did you mean…”* suggestions and a hint.

### Paths and imports
- `src/_pathsetup.py` registers the source root and every phase folder on `sys.path`, so modules import each other by short name (`from errors import …`, `from ast_nodes import …`).
- It is invoked by the entry points (`main.py`, `conftest.py`, `ide/engine.py`) and at the top of each module file so the module is self-contained.
- The `src/interpreter/` package remains a **re-export façade** that re-exports the public surface (`Interpreter`, `Function`, `compile_program`, `run_source`, `parse_program`, `parse_program_collecting`, `parse_expression`) from its new locations, so external call sites stay stable.

### Tests
Run `pytest` from the project root; `conftest.py` configures the paths automatically. The suites build ASTs directly, so they work even before the ANTLR parser is generated.

---

## 5. Installation & Running

> **User Guide (sections 5–7):** how to run the program from scratch, and every command and task the language supports.
### Requirements
- Python 3.10+
- `antlr4-python3-runtime`, `sympy`, `numpy`, `matplotlib`, `scipy`, `prompt_toolkit`, `rich`, `pytest`
- `PySide6` *(optional)* — enables the true-RTL Qt editor; without it the IDE falls back to Tkinter.

### Setup
```bash
pip install -r requirements.txt

# Generate the parser from the grammar (needs Java + the antlr4 tool):
antlr4 -Dlanguage=Python3 -visitor -o generated HassoobArabi.g4
```

### Running
```bash
python main.py                     # interactive REPL
python main.py examples/مرحبا.حع    # run a source file
python main.py -c "اطبع(٣+٤)"       # run a single expression
python main.py --ide               # launch the graphical IDE
python -m ide                      # (equivalent) launch the IDE
```

---

## 6. Language Reference

### 6.1 Numerals, comments, and statements
- **Numerals:** Arabic-Indic (`٠١٢٣٤٥٦٧٨٩`) and Western (`0-9`) digits are both valid. Floating point requires an ASCII dot: `٢.٥`.
- **Statements** end at a newline; an optional terminator `;` or the Arabic semicolon `؛` is allowed.
- **Comments:** `# ...` (line), `ملاحظة ...` (Arabic line comment), `/* ... */` (block).

### 6.2 Variables & assignment
```text
أ = ٧                 # assignment
أ += ٣                # augmented assignment: += -= *= /= %= ^= ++=
النص ++= "!"          # ++= appends to a string
```
The interpreter uses a **Mathematica-style scope chain**: functions introduce a new scope and resolve free names against enclosing scopes.

### 6.3 Data types
| Type | `نوع` returns | Example |
|---|---|---|
| Number | `عدد` | `٣`, `٢.٥`, `-٧` |
| Boolean | `منطقي` | `صح`, `خطأ` |
| String | `نص` | `"مرحبا"`, `'نص'` |
| Null | `فارغ` | `فارغ` |
| List | `قائمة` | `[١, ٢, ٣]` |
| Matrix / array | `مصفوفة` | `[[١,٢],[٣,٤]]` (via numeric ops) |
| Symbolic | `رمزي` | result of `رمز س` |
| Function | `دالة` | a `دالة` or lambda |

### 6.4 Operators
| Category | Operators |
|---|---|
| Arithmetic | `+`  `-`  `*`  `/`  `%` (mod)  `^` (power)  `÷` (integer division) |
| Matrix | `**` (matrix multiply) |
| String | `++` (concatenation — formats both sides) |
| Comparison | `==`  `!=`/`≠`  `<`  `<=`/`≤`  `>`  `>=`/`≥` (chainable: `٦٠ <= د < ٩٠`) |
| Logical | `و`/`&&` (and)  `أو`/`\|\|` (or)  `ليس`/`!` (not) |
| Assignment | `=`  `+=`  `-=`  `*=`  `/=`  `%=`  `^=`  `++=` |
| Lambda arrow | `=>` |

**Symbolic constants:** `باي` / `π`, `هـ` (Euler's *e*), `لانهاية` (infinity).

### 6.5 Control flow
```text
# Conditional
إذا (أ > ب) {
    اطبع("أكبر")
} وإلا إذا (أ == ب) {
    اطبع("متساوٍ")
} وإلا {
    اطبع("أصغر")
}

# While loop
بينما (س < ١٠) { س += ١ }

# For-each over a sequence
لكل عنصر في [١, ٢, ٣] { اطبع(عنصر) }

# For-range (inclusive of both ends; optional بخطوة step)
لكل ع من ١ إلى ٥ { اطبع(ع) }
لكل ع من ١٠ إلى ١ بخطوة -٢ { اطبع(ع) }
```
`توقف` = break, `استمر` = continue.

### 6.6 Functions & lambdas
```text
دالة مربع(س) {
    إرجع س * س
}

دالة عاملي(ن) {
    إذا (ن <= ١) { إرجع ١ }
    إرجع ن * عاملي(ن - ١)     # recursion
}

# Lambdas: single param without parentheses, or (a, b) => ...
مضاعف = س => س * ٢
جمع    = (أ, ب) => أ + ب
```

### 6.7 Strings & f-strings
```text
الاسم = "جعفر"
اطبع("مرحبًا يا " ++ الاسم)            # ++ concatenation
اطبع(f"الطول هو {طول(الاسم)} حروف")   # f-string interpolation
```
Escapes: `\n \t \\ \" \' \uXXXX`. f-strings start with `f`, `F`, or `ف`.

### 6.8 Lists, indexing & index assignment
```text
أ = [[١, ٢, ٣], [٤, ٥, ٦]]
اطبع(أ[٠][١])          # chained index read on a list  → ٢
أ[٠][٠] = ٩            # chained index assignment
م = نقل(أ)             # numpy array (matrix)
اطبع(م[٠, ١])          # N-D comma index — only on matrices/arrays
```
> **Note:** the comma form `م[ص, ع]` produces a tuple key and works **only on matrices/arrays** (e.g. results of `نقل`, `معكوس`). For plain lists use chained `أ[ص][ع]`.

### 6.9 Symbolic mathematics
```text
رمز س
د = س^٣ - ٦*س^٢ + ٩*س
اطبع("المشتقة:", اشتق(د, س))        # 3·س² − 12·س + 9
اطبع("التكامل:", كامل(د, س))
اطبع("الجذور:", حل(د, س))
اطبع("النهاية:", نهاية((س^٢-١)/(س-١), س, ١))   # 2
```

---

### 6.10 Normalization — and why we do NOT normalize hamzas

Before lexing, source code passes through a **normalization** step in `src/frontend/parsing.py` (the `_strip_tashkeel` function) whose goal is that the same token written in several ways is read as one word:

- **Diacritics (tashkeel) and tatweel:** diacritics (fatha, damma, kasra, shadda, sukun…) and the tatweel mark (ـ) are stripped **outside strings and comments**, so ‹إذِا›, ‹إذّا› and ‹إذا› are all read as the keyword `إذا`.
- **Digits:** both Arabic-Indic digits (`٠–٩`) and Western digits (`0–9`) are accepted in source, and all output is normalized to Arabic digits.
- **Strings and comments are copied verbatim:** any diacritics inside a string literal `"..."` / `'...'` or inside a comment (`#`, `/* */`, `ملاحظة`) are preserved, because they may be intentional.

**Why we intentionally do not normalize hamzas:** common Arabic normalization unifies the hamza forms (أ, إ, آ, ء) into a plain alif, but that would corrupt the language's own words — `خطأ` (“false”) would become `خطا`, and `اقرأ` (“read”) would become `اقرا`. Because `خطأ` and `اقرأ` are core words in the language (a boolean value and a builtin name), we **strip only diacritics and tatweel and never change letter forms**, preserving the identity and correctness of the keywords. This gives flexibility in typing (ignoring diacritics and tatweel) without touching the integrity of the language's vocabulary.

---

## 7. Built-in Function Catalog

### Output
| Command | Description |
|---|---|
| `اطبع(...)` | Print one or more values to the console (always in Arabic numerals). |

### Symbolic mathematics
| Command | Description |
|---|---|
| `بسط(تعبير)` | Simplify an expression. |
| `وسع(تعبير)` | Expand (e.g. multiply out products). |
| `حلل(تعبير)` | Factor an expression. |
| `عوض(تعبير, رمز, قيمة)` | Substitute a value for a symbol. |
| `اشتق(تعبير, رمز[, رتبة])` | Differentiate (optional order). |
| `كامل(تعبير, رمز[, أ, ب])` | Integrate — indefinite, or definite over `[أ, ب]`. |
| `نهاية(تعبير, رمز, نقطة)` | Limit at a point. |
| `متسلسلة(تعبير, رمز[, حول, رتبة])` | Taylor/Maclaurin series. |
| `حل(معادلة, رمز)` | Solve an equation. |
| `حل_منظومة(معادلات, رموز)` | Solve a system of equations. |
| `حل_تفاضلي(معادلة, دالة)` | Solve an ODE. |

### Numeric & linear algebra
| Command | Description |
|---|---|
| `جذر_عددي(دالة, رمز, تخمين)` | Numeric root (Newton's method). |
| `نقل(مصفوفة)` | Transpose. |
| `محدد(مصفوفة)` | Determinant. |
| `معكوس(مصفوفة)` | Inverse. |
| `قيم_ذاتية(مصفوفة)` | Eigenvalues. |
| `ضرب_نقطي(ش١, ش٢)` | Dot product. |
| `ضرب_متجهي(ش١, ش٢)` | Cross product. |
| `حل_خطي(أ, ب)` | Solve the linear system A·x = b. |

### Trigonometry
| Command | Description |
|---|---|
| `جا(زاوية)` / `جيب(زاوية)` | Sine; angle in radians. Works numerically and symbolically. |
| `جتا(زاوية)` / `جيب_تمام(زاوية)` | Cosine; angle in radians. Works numerically and symbolically. |

### Statistics
| Command | Description |
|---|---|
| `متوسط` | Mean. |
| `وسيط` | Median. |
| `تباين` | Variance. |
| `انحراف_معياري` | Standard deviation. |
| `أصغر` / `أكبر` | Min / max. |
| `مدى` | Range (max − min). |
| `مجموع` / `ناتج` | Sum / product. |
| `ارتباط(س, ع)` | Correlation coefficient. |
| `عشوائي(...)` | Random number(s). |

### Plotting
| Command | Description |
|---|---|
| `ارسم(تعبير[, مدى])` | Plot an expression/function. |
| `ارسم_وسيط(...)` | Parametric plot. |
| `ارسم_ثلاثي(...)` | 3-D plot. |
| `ارسم_بيانات([xs, ys], نوع="نقاط"/"خط", عنوان=)` | Plot data points / line. |
| `مدرج_تكراري(بيانات[, عدد], عنوان=)` | Histogram. |
| `مخطط_أعمدة(...)` | Bar chart. |

### Lists & strings
| Command | Description |
|---|---|
| `طول(x)` | Length. |
| `قطعة(تسلسل, بداية, نهاية)` | Slice. |
| `استبدل(نص, قديم, جديد)` | Replace. |
| `قسم(نص[, فاصل])` | Split. |
| `دمج(قائمة[, فاصل])` | Join. |
| `نوع(x)` | Type name (`عدد`, `نص`, `قائمة`, …). |
| `قائمة_من(بداية, نهاية[, خطوة])` | Range list (inclusive). |
| `ترتيب(قائمة[, عكسي=])` | Sort (optionally descending). |
| `عكس(تسلسل)` | Reverse. |
| `طبق(دالة, قائمة)` | Map. |
| `صفي` / `اختر(دالة, قائمة)` | Filter. |

---

## 8. Error Handling

The language adopts an explicit principle: **surface every possible error at once, and do not stop at the first one.** Instead of fixing one error only to discover the next on the following run, the user gets a complete list every run.

Every error is a fully Arabic message in the standard format:

```
خطأ في السطر {line}، العمود {col}: {message}
   ↪ هل تقصد ‹suggestion›؟
   💡 {hint}
```

**Collecting errors across phases (no stop-at-first):**

- **Parse phase:** `parse_program_collecting` gathers all the syntax/lexical errors ANTLR reports in a single pass, instead of stopping at the first.
- **Semantic phase:** `src/midend/semantic.py` keeps checking the rest of the program after each error and collects them all, then raises them together via `MultiError` (or a single error if there is only one). Broken spots are also represented by inert `ErrorNode`s that do not abort the rest of the analysis.
- This way the user sees a **complete map** of what needs fixing before re-running.

The error hierarchy (organised in `src/errors/`) distinguishes four categories, each with its own icon and label:

| Category | Module | Label | Icon | Raised when |
|---|---|---|---|---|
| Lexical | `errors/syntax.py` (`LexError`) | `خطأ لفظي` | 🔤 | invalid token / character. |
| Syntax | `errors/syntax.py` (`ParseError`) | `خطأ نحوي` | 📝 | source violates the grammar. |
| Semantic | `errors/semantic.py` (`SemanticError`, `MultiError`) | `خطأ دلالي` | 🔍 | undefined name, wrong arg count, etc. |
| Runtime | `errors/runtime.py` (`HassoobRuntimeError`) | `خطأ في التنفيذ` | ⚠️ | division by zero, invalid type, etc. |

**Why we report an undefined name once per scope:** if a mistyped name (say `العدّاد`) is used ten times inside a function, reporting it ten times floods the list with duplicate messages for a single error whose root is one missing definition line. So each undefined name is reported **once per scope** (the function, or the top level): the set of reported names is kept and reset on entering each function body, so an error in one function does not silence the same name in another. This is the mature-compiler model (like GCC): one clear message per name per scope.

At the same time, the error carries the symbol name (`err.symbol`), so the IDE highlights **every** occurrence of that name with a red underline; the user sees one uncluttered message in the list yet can still see all the places that need fixing.

Control-flow signals (`إرجع`, `توقف`, `استمر`, in `errors/signals.py`) are deliberately **not** part of the error hierarchy, so they are never swallowed by user error handlers.

---

## 9. Example Programs

The five programs in `examples/` together exercise the entire language. Run each with `python main.py examples/<file>`. *(Outputs are printed with Arabic numerals.)*

- **① `مرحبا.حع` — A gentle introduction.** Printing, variables, the six arithmetic operators, string length + `++` concatenation + f-strings, a user-defined function, an `إذا/وإلا` conditional, and a `لكل … من … إلى` loop.
- **② `إحصاء.حع` — Data analysis.** All statistics functions, sorting + slicing, `اختر`/`طبق` lambdas, a multi-branch grading function, correlation, and two plots (histogram + scatter).
- **③ `حساب_تفاضلي.حع` — Calculus toolkit.** Factoring, 1st/2nd derivatives, critical points via `حل`, the second-derivative test (`عوض`), indefinite & definite integrals, a 0/0 limit, a Taylor series, a numeric root, and a plot of `د(س) = س³ − ٦س² + ٩س` with its derivative.
- **④ `مصفوفات.حع` — Linear algebra.** Matrix multiply (`**`), transpose, determinant, inverse, eigenvalues, the N-D comma index `[ص, ع]`, chained index assignment, `حل_خطي`, dot & cross products.
- **⑤ `خوارزميات.حع` — Control flow & algorithms.** Recursion (factorial), `بينما` + augmented assignment (Fibonacci), an early-return prime test, `توقف`/`استمر`, palindrome detection via `عكس`, `قسم`/`دمج`, `طبق`/`اختر` lambdas, chained comparisons, and `نوع` type checks.

---

## 10. Tests

```bash
pytest tests/
# Each suite also runs standalone and builds ASTs directly,
# so tests pass even before the ANTLR parser is generated:
python tests/test_interpreter.py
python tests/test_optimizer.py
python tests/test_builtins.py
```

The test suites import through the package names (`from interpreter import …`, `from ast_nodes import …`, `from errors import …`), which the new packages re-export unchanged — so the modular refactor required **no test changes**.

> Tip: after pulling the refactor, clear stale bytecode if you see import errors:
> `find . -name __pycache__ -type d -exec rm -rf {} +`

---

## 11. Future Work

> *Ideas for developers:* this section gathers what can be added to the language later, and what we would have added with more time. The three-layer structure (front / middle / back end) makes each of these a natural, localized addition.

### 1. Complex numbers
Support complex numbers `أ + ب ت` (where `ت` is the imaginary unit), with arithmetic on them and companion functions such as real part, imaginary part, conjugate, and magnitude. This mainly touches the back end: a new value type in `src/backend/`, operator semantics in `runtime_ops.py`, and functions in `library/numeric.py`, plus normalization of the imaginary-unit symbol in the front end.

### 2. An `إلى_تعبير` function (string → expression, like Mathematica's `ToExpression`)
A function that takes a string and returns its value after parsing and evaluating it — to turn strings into numbers, or even into full symbolic expressions. It reuses the existing front end (`parse_expression`) and then goes through back-end evaluation, so no grammar change is needed.

### 3. Translating every error into Arabic
We already translate most ANTLR errors into friendly Arabic messages, but some cases still surface in English (from ANTLR or Python), and we aim to catch them all and render them in our unified Arabic format. One example not yet translated — a positional argument placed after a named one:

> After the **named** argument عنوان="التوزيع التكراري", you put a **positional** argument 8 (separated by the Arabic comma ،). A positional argument is not allowed to come after a named one.

The goal is an Arabic message in our canonical format, e.g.:

```
خطأ في السطر {line}، العمود {col}: لا يجوز وضع وسيط موضعي (٨) بعد وسيط مُسمّى (عنوان="التوزيع التكراري").
   ↪ انقل الوسيط الموضعي قبل الوسطاء المُسمّاة.
   💡 رتّب الوسطاء: الموضعية أولًا ثم المُسمّاة.
```

### 4. A VS Code extension
An official extension for the language in Visual Studio Code: syntax highlighting via a TextMate grammar for `.حع` files, autocompletion for keywords and builtins, and live error highlighting through a language server (LSP) that reuses the existing diagnostics engine in `ide/engine.py`, with right-to-left (RTL) support.

Contributions from developers on any of these fronts are welcome.

---

## 12. Repository & Team

- **Repository:** https://github.com/The-Merge-Conflict/Hassoob-Arabi
- **Team:** Jaafer Mahfoud · Laila Al-Abdullah · Hatem Ibrahim
- **Course:** Compilers — language design & implementation project.
