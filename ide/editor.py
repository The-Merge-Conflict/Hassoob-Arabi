# ───────────────────────────────────────────────────────────────────────────
# ide/editor.py
# بيئة التطوير الرسومية لحاسوب عربي (Tkinter) — محرّر يميني (RTL)
# مع تلوين للبنية، أرقام أسطر، وطرفيّة (REPL) تفاعلية بالعربية.
#
# Tkinter ships with CPython, so the IDE runs offline with no extra packages.
# All execution is delegated to ide.engine.HassoobEngine; all colouring to
# ide.highlight.Highlighter — both Tkinter-free and unit-tested.
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import os
import sys

# Ensure plots open as real, interactive Matplotlib windows (with the save /
# zoom / pan navigation toolbar) instead of a headless backend. This MUST run
# before importing the engine, which transitively imports matplotlib.pyplot.
os.environ.setdefault("HASSOOB_IDE", "1")
try:
    import matplotlib as _matplotlib
    _matplotlib.use("TkAgg", force=True)    
except Exception:
    pass

from .engine import HassoobEngine
from .highlight import Highlighter

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, font as tkfont
except Exception as exc:  # pragma: no cover - tkinter missing
    raise SystemExit(
        "لا تتوفّر مكتبة Tkinter الرسومية.\n"
        "على لينكس ثبّتها بـ: sudo apt install python3-tk\n"
        f"(التفصيل: {exc})"
    )


# ── theme (a calm, cute palette) ──────────────────────────────────────
BG       = "#1e1f2b"
BG_ALT   = "#262838"
GUTTER   = "#2c2e40"
FG       = "#e7e7ef"
ACCENT   = "#c792ea"
COLORS = {
    "comment":  "#6b7089",
    "string":   "#9ece6a",
    "number":   "#ff9e64",
    "keyword":  "#bb9af7",
    "constant": "#f7768e",
    "builtin":  "#7dcfff",
    "operator": "#89ddff",
}
OUT_COLORS = {
    "out":   FG,
    "err":   "#ff6b8b",
    "repl":  "#7dcfff",
    "value": "#9ece6a",
    "info":  "#c792ea",
}

EXT = ".\u062d\u0639"  # امتداد ملفات حاسوب عربي

SAMPLE = (
    "ملاحظة مرحبًا بك في حاسوب عربي!\n"
    "اطبع(\"أهلًا وسهلًا 🌸\")\n\n"
    "دالة مربّع(س) {\n"
    "    إرجع س * س\n"
    "}\n\n"
    "لكل ع من ١ إلى ٥ {\n"
    "    اطبع(مربّع(ع))\n"
    "}\n"
)


class LineNumbers(tk.Canvas):
    """A right-aligned gutter that mirrors the editor's visible lines."""

    def __init__(self, master, text_widget, **kw):
        super().__init__(master, width=52, bg=GUTTER, highlightthickness=0, **kw)
        self.text = text_widget
        self.font = tkfont.Font(font=text_widget["font"])

    def redraw(self, *_):
        self.delete("all")
        i = self.text.index("@0,0")
        while True:
            info = self.text.dlineinfo(i)
            if info is None:
                break
            y = info[1]
            line = i.split(".")[0]
            self.create_text(
                int(self["width"]) - 8, y,
                anchor="ne", text=line, fill="#6b7089", font=self.font,
            )
            i = self.text.index(f"{i}+1line")


class HassoobIDE:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = HassoobEngine()
        self.highlighter = Highlighter(self.engine.builtin_names)
        self.current_path = None
        self._hl_job = None

        root.title("حاسوب عربي — بيئة التطوير المتكاملة")
        root.geometry("1040x720")
        root.configure(bg=BG)

        self.code_font = self._pick_font(size=15)
        self.term_font = self._pick_font(size=13)

        self._build_menu()
        self._build_toolbar()
        self._build_body()
        self._build_statusbar()
        self._bind_keys()

        self.editor.insert("1.0", SAMPLE)
        self.highlight_now()
        self.lines.redraw()
        self._println(
            "جاهز. اكتب شفرتك ثم اضغط ▶ تشغيل (F5)، أو جرّب الطرفيّة بالأسفل.",
            "info",
        )

    # ── fonts ────────────────────────────────────────────────────
    def _pick_font(self, size: int) -> tkfont.Font:
        available = set(tkfont.families())
        for name in ("Amiri", "Scheherazade New", "Noto Naskh Arabic",
                     "Noto Sans Arabic", "DejaVu Sans Mono", "Courier New"):
            if name in available:
                return tkfont.Font(family=name, size=size)
        return tkfont.Font(family="TkFixedFont", size=size)

    # ── menu ─────────────────────────────────────────────────────
    def _build_menu(self):
        bar = tk.Menu(self.root)
        m_file = tk.Menu(bar, tearoff=0)
        m_file.add_command(label="جديد", accelerator="Ctrl+N", command=self.new_file)
        m_file.add_command(label="فتح…", accelerator="Ctrl+O", command=self.open_file)
        m_file.add_command(label="حفظ", accelerator="Ctrl+S", command=self.save_file)
        m_file.add_command(label="حفظ باسم…", command=self.save_file_as)
        m_file.add_separator()
        m_file.add_command(label="خروج", command=self.root.quit)
        bar.add_cascade(label="ملف", menu=m_file)

        m_run = tk.Menu(bar, tearoff=0)
        m_run.add_command(label="▶ تشغيل", accelerator="F5", command=self.run_code)
        m_run.add_command(label="مسح المخرجات", command=self.clear_output)
        m_run.add_command(label="↺ جلسة جديدة", command=self.reset_session)
        bar.add_cascade(label="تشغيل", menu=m_run)

        m_help = tk.Menu(bar, tearoff=0)
        m_help.add_command(label="الدوال المدمجة", command=self.show_builtins)
        m_help.add_command(label="حول…", command=self.show_about)
        bar.add_cascade(label="مساعدة", menu=m_help)
        self.root.config(menu=bar)

    # ── toolbar ────────────────────────────────────────────────
    def _build_toolbar(self):
        bar = tk.Frame(self.root, bg=BG_ALT)
        bar.pack(side="top", fill="x")
        # RTL: pack buttons from the right.
        specs = [
            ("▶ تشغيل", self.run_code, ACCENT),
            ("جديد", self.new_file, None),
            ("فتح", self.open_file, None),
            ("حفظ", self.save_file, None),
            ("مسح", self.clear_output, None),
            ("↺ جلسة", self.reset_session, None),
        ]
        for label, cmd, color in specs:
            b = tk.Button(
                bar, text=label, command=cmd, relief="flat",
                bg=(color or BG_ALT), fg=("#1e1f2b" if color else FG),
                activebackground=ACCENT, activeforeground="#1e1f2b",
                font=(self.term_font.actual("family"), 11, "bold"),
                padx=12, pady=6, cursor="hand2", bd=0,
            )
            b.pack(side="right", padx=3, pady=4)

    # ── body: editor (top) + terminal (bottom) ────────────────────────────
    def _build_body(self):
        pane = tk.PanedWindow(
            self.root, orient="vertical", bg=BG, sashwidth=6, sashrelief="flat",
            bd=0,
        )
        pane.pack(fill="both", expand=True)

        # —— editor frame ——
        ed = tk.Frame(pane, bg=BG)
        scroll = tk.Scrollbar(ed, orient="vertical")
        scroll.pack(side="left", fill="y")  # RTL: scrollbar on the left
        self.editor = tk.Text(
            ed, wrap="none", undo=True, bg=BG, fg=FG, insertbackground=ACCENT,
            selectbackground="#3b3f5c", font=self.code_font, bd=0,
            padx=12, pady=10, yscrollcommand=self._on_scroll,
            tabs=("1c",), spacing1=2, spacing3=2,
        )
        self.editor.tag_configure("all", justify="right")
        self._install_rtl_proxy()
        self.lines = LineNumbers(ed, self.editor)
        self.lines.pack(side="right", fill="y")
        self.editor.pack(side="right", fill="both", expand=True)
        scroll.config(command=self.editor.yview)
        self._vscroll = scroll
        for tag, color in COLORS.items():
            self.editor.tag_configure(tag, foreground=color)
        pane.add(ed, height=420)

        # —— terminal frame ——
        term = tk.Frame(pane, bg=BG_ALT)
        header = tk.Label(
            term, text="الطرفيّة / المخرجات", bg=BG_ALT, fg="#6b7089",
            anchor="e", font=(self.term_font.actual("family"), 10, "bold"),
        )
        header.pack(side="top", fill="x", padx=8, pady=(4, 0))
        oscroll = tk.Scrollbar(term, orient="vertical")
        oscroll.pack(side="left", fill="y")
        self.output = tk.Text(
            term, wrap="word", bg="#16171f", fg=FG, font=self.term_font,
            bd=0, padx=12, pady=8, height=10, state="disabled",
            yscrollcommand=oscroll.set,
        )
        self.output.tag_configure("all", justify="right")
        for tag, color in OUT_COLORS.items():
            self.output.tag_configure(tag, foreground=color)
        self.output.pack(side="right", fill="both", expand=True)
        oscroll.config(command=self.output.yview)

        # REPL input row
        row = tk.Frame(term, bg=BG_ALT)
        row.pack(side="bottom", fill="x")
        self.repl = tk.Entry(
            row, bg="#16171f", fg=FG, insertbackground=ACCENT,
            font=self.term_font, bd=0, justify="right",
        )
        self.repl.pack(side="right", fill="x", expand=True, padx=(8, 4), pady=6,
                       ipady=5)
        prompt = tk.Label(
            row, text="حاسوب عربي ←", bg=BG_ALT, fg=ACCENT,
            font=(self.term_font.actual("family"), 12, "bold"),
        )
        prompt.pack(side="right", padx=(4, 8))
        self.repl.bind("<Return>", self._on_repl_enter)
        pane.add(term)

    # ── status bar ───────────────────────────────────────────────
    def _build_statusbar(self):
        self.status = tk.Label(
            self.root, text="جاهز", bg=BG_ALT, fg="#6b7089", anchor="e",
            font=(self.term_font.actual("family"), 10), padx=10,
        )
        self.status.pack(side="bottom", fill="x")

    # ── key bindings ───────────────────────────────────────────
    def _bind_keys(self):
        self.editor.bind("<<TextModified>>", self._on_modified)
        self.editor.bind("<KeyRelease>", lambda e: self._update_status())
        self.editor.bind("<ButtonRelease>", lambda e: self._update_status())
        self.editor.bind("<Configure>", lambda e: self.lines.redraw())
        self.editor.bind("<MouseWheel>", lambda e: self.root.after(1, self.lines.redraw))
        self.editor.bind("<Button-4>", lambda e: self.root.after(1, self.lines.redraw))
        self.editor.bind("<Button-5>", lambda e: self.root.after(1, self.lines.redraw))
        self.root.bind("<F5>", lambda e: self.run_code())
        self.root.bind("<Control-r>", lambda e: self.run_code())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-n>", lambda e: self.new_file())

    def _on_scroll(self, *args):
        # Keep the scrollbar thumb in sync with the editor and repaint the
        # line-number gutter.
        if hasattr(self, "_vscroll"):
            self._vscroll.set(*args)
        self.lines.redraw()

    def _install_rtl_proxy(self):
        """Intercept the Text widget's low-level command so every edit is
        right-justified in the SAME operation — making Arabic text RTL-aligned
        from the very first character, with no momentary left-to-right flicker.
        """
        w = self.editor
        self._orig_widget = str(w) + "_orig"
        w.tk.call("rename", str(w), self._orig_widget)
        w.tk.createcommand(str(w), self._editor_proxy)

    def _editor_proxy(self, *args):
        try:
            result = self.editor.tk.call((self._orig_widget,) + args)
        except tk.TclError:
            return ""
        if args and args[0] in ("insert", "delete", "replace"):
            # Re-apply right-justification via the ORIGINAL widget command (so we
            # don't re-enter this proxy), within the same edit operation.
            self.editor.tk.call(self._orig_widget, "tag", "add", "all", "1.0", "end")
            self.editor.event_generate("<<TextModified>>", when="tail")
        return result

    def _on_modified(self, _evt=None):
        self.schedule_highlight()
        self.lines.redraw()
        self._update_status()

    # ── highlighting ────────────────────────────────────────────
    def schedule_highlight(self):
        if self._hl_job is not None:
            self.root.after_cancel(self._hl_job)
        self._hl_job = self.root.after(120, self.highlight_now)

    def highlight_now(self):
        self._hl_job = None
        text = self.editor.get("1.0", "end-1c")
        for tag in COLORS:
            self.editor.tag_remove(tag, "1.0", "end")
        for span in self.highlighter.spans(text):
            start = f"1.0+{span.start}c"
            end = f"1.0+{span.end}c"
            self.editor.tag_add(span.tag, start, end)
        # keep right-justification applied to the whole document
        self.editor.tag_add("all", "1.0", "end")

    # ── running ─────────────────────────────────────────────────
    def run_code(self):
        source = self.editor.get("1.0", "end-1c")
        self._println("─" * 30, "info")
        self._println("▶ تشغيل البرنامج…", "info")
        res = self.engine.run_source(source, fresh=True)
        if res.output:
            self._print(res.output, "out")
        if res.error:
            self._println(res.error, "err")
        elif not res.output:
            self._println("(انتهى بدون مخرجات)", "info")
        self.status.config(text=("✔ تم بنجاح" if res.ok else "✖ انتهى بخطأ"))

    def _on_repl_enter(self, _evt=None):
        line = self.repl.get().strip()
        if not line:
            return "break"
        self.repl.delete(0, "end")
        self._println(f"← {line}", "repl")
        res = self.engine.eval_line(line)
        if res.output:
            self._print(res.output, "out")
        if res.error:
            self._println(res.error, "err")
        elif res.value is not None:
            self._println(f"← {res.value}", "value")
        return "break"

    # ── output helpers ───────────────────────────────────���───���───
    def _print(self, text: str, tag: str = "out"):
        self.output.config(state="normal")
        self.output.insert("end", text, (tag, "all"))
        self.output.see("end")
        self.output.config(state="disabled")

    def _println(self, text: str, tag: str = "out"):
        self._print(text + "\n", tag)

    def clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")

    def reset_session(self):
        self.engine.reset()
        self._println("↺ بدأت جلسة جديدة (تم مسح كل المتغيّرات والدوال).", "info")

    # ── file ops ────────────────────────────────────────────────
    def _filetypes(self):
        return [("ملفات حاسوب عربي", f"*{EXT}"), ("كل الملفات", "*.*")]

    def new_file(self):
        self.editor.delete("1.0", "end")
        self.current_path = None
        self.highlight_now()
        self.lines.redraw()
        self._update_status()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=self._filetypes())
        if not path:
            return
        with open(path, "r", encoding="utf-8") as fh:
            data = fh.read()
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", data)
        self.current_path = path
        self.highlight_now()
        self.lines.redraw()
        self._update_status()

    def save_file(self):
        if not self.current_path:
            return self.save_file_as()
        with open(self.current_path, "w", encoding="utf-8") as fh:
            fh.write(self.editor.get("1.0", "end-1c"))
        self.status.config(text=f"حُفِظ: {os.path.basename(self.current_path)}")

    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=EXT, filetypes=self._filetypes())
        if not path:
            return
        self.current_path = path
        self.save_file()
        self._update_status()

    # ── help dialogs ───────────────────────────────────────────
    def show_builtins(self):
        names = "، ".join(self.engine.builtin_names)
        messagebox.showinfo("الدوال المدمجة", names or "(لا توجد)")

    def show_about(self):
        messagebox.showinfo(
            "حول حاسوب عربي",
            "حاسوب عربي — بيئة تطوير متكاملة للغة برمجة عربية.\n"
            "محرّر يميني (RTL) مع تلوين وطرفيّة تفاعلية 🌸",
        )

    # ── status ────────────────────────────────────────────────
    def _update_status(self):
        idx = self.editor.index("insert")
        line, col = idx.split(".")
        name = os.path.basename(self.current_path) if self.current_path else "ملف جديد"
        self.status.config(text=f"{name}    •    السطر {line}، العمود {int(col)+1}")


def launch():
    """تشغيل بيئة التطوير / open the IDE window."""
    root = tk.Tk()
    HassoobIDE(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    launch()
