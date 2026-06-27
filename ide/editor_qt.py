# ───────────────────────────────────────────────────────────────────────────
# ide/editor_qt.py
# بيئة تطوير رسومية يمينية (RTL) حقيقية لحاسوب عربي — مبنيّة على Qt (PySide6).
#
# لماذا Qt؟  مكوّن النص في Tkinter يدعم "محاذاة" لليمين فقط، لا "اتجاه فقرة"
# يمينيًّا، فتظهر استدعاءات مثل  اطبع("...")  بترتيب معكوس.  أمّا Qt فيطبّق
# خوارزمية Unicode للاتجاهين بالكامل، ويكفي ضبط اتجاه التخطيط إلى RightToLeft
# ليصبح المحرّر يمينيًّا صحيحًا منذ أوّل حرف.
#
# المحرّك (engine) والمُلوِّن (highlight) خاليان من أيّ اعتماد على واجهة، لذا
# يُعاد استخدامهما هنا كما هما.  إن لم تتوفّر PySide6 تُرفَع ImportError ليتحوّل
# المُشغِّل تلقائيًّا إلى واجهة Tkinter البديلة.
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import html as _html
import os
import sys

# الرسوم: افتح نوافذ Matplotlib أصيلة (بشريط أدوات الحفظ/التكبير) عبر QtAgg.
# يجب ضبط الواجهة الخلفية قبل أوّل إنشاء لشكل بياني.
os.environ.setdefault("HASSOOB_IDE", "1")
try:
    import matplotlib as _matplotlib
    _matplotlib.use("QtAgg", force=True)
except Exception:
    pass

# PySide6 أولًا: إن غابت، ارفع ImportError كي يتراجع المُشغِّل إلى Tkinter.
try:
    from PySide6.QtCore import Qt, QRect, QSize, QTimer
    from PySide6.QtGui import (
        QAction, QColor, QFont, QKeySequence, QPainter,
        QSyntaxHighlighter, QTextCharFormat, QTextCursor, QTextOption, QPalette,
    )
    from PySide6.QtWidgets import (
        QApplication, QFileDialog, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QMessageBox, QPlainTextEdit, QSplitter, QTextEdit,
        QToolBar, QVBoxLayout, QWidget,
    )
except Exception as exc:  # PySide6 غير مُثبّتة
    raise ImportError("PySide6 is required for the Qt RTL IDE") from exc

from .engine import HassoobEngine
from .highlight import Highlighter


# ── السمة (لوحة ألوان هادئة لطيفة) ────────────────────────────────────
BG       = "#1e1f2b"
BG_ALT   = "#262838"
GUTTER   = "#2c2e40"
FG       = "#e7e7ef"
ACCENT   = "#c792ea"
MUTED    = "#6b7089"
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
    "اطبع(\"أهلًا وسهلًا \")\n\n"
    "دالة مربّع(س) {\n"
    "    إرجع س * س\n"
    "}\n\n"
    "لكل ع من ١ إلى ٥ {\n"
    "    اطبع(مربّع(ع))\n"
    "}\n"
)

_FONT_CANDIDATES = (
    "Amiri", "Scheherazade New", "Noto Naskh Arabic",
    "Noto Sans Arabic", "DejaVu Sans Mono", "Courier New", "monospace",
)


def _arabic_font(size: int = 14) -> QFont:
    f = QFont()
    f.setFamilies(list(_FONT_CANDIDATES))
    f.setPointSize(size)
    f.setStyleStrategy(QFont.PreferAntialias)
    return f


def _apply_rtl_text(widget) -> None:
    """فرض اتجاه فقرة يميني (RTL) حقيقي + محاذاة يمين على حقل نصيّ.

    الاكتفاء بـ setLayoutDirection() لا يكفي: فهو يضبط إطار العنصر فقط
    (أشرطة التمرير والهوامش) ولا يغيّر اتجاه فقرات النصّ نفسها.  لذلك نضبط
    خيار النصّ الافتراضي للمستند إلى RTL ليصير اتجاه كل الأسطر يمينيًا.
    """
    widget.setLayoutDirection(Qt.RightToLeft)
    doc = widget.document()
    opt = doc.defaultTextOption()
    opt.setTextDirection(Qt.RightToLeft)
    opt.setAlignment(Qt.AlignRight)
    doc.setDefaultTextOption(opt)


# ── المُلوِّن النحوي (يعيد استخدام ide.highlight) ──────────────────────
class QtHighlighter(QSyntaxHighlighter):
    def __init__(self, document, builtin_names):
        super().__init__(document)
        self.hl = Highlighter(builtin_names)
        self.formats = {}
        for tag, color in COLORS.items():
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            if tag in ("keyword", "constant"):
                fmt.setFontWeight(QFont.Bold)
            if tag == "comment":
                fmt.setFontItalic(True)
            self.formats[tag] = fmt

    def highlightBlock(self, text):  # noqa: N802 (Qt override)
        for span in self.hl.spans(text):
            fmt = self.formats.get(span.tag)
            if fmt is not None:
                self.setFormat(span.start, span.end - span.start, fmt)


# ── منطقة أرقام الأسطر (على اليمين، كما يليق بمحرّر عربي) ──────────────
class _LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):  # noqa: N802
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):  # noqa: N802
        self.editor.paint_line_numbers(event)


class CodeEditor(QPlainTextEdit):
    """محرّر يميني مع شريط أرقام أسطر على اليمين."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(" "))
        # الإصلاح الجوهري: اتجاه فقرة يمينيّ حقيقي — لا مجرّد محاذاة.
        _apply_rtl_text(self)
        self._gutter = _LineNumberArea(self)
        self.blockCountChanged.connect(lambda _=0: self._update_width())
        self.updateRequest.connect(self._on_update)
        self._update_width()

    # عرض الشريط بحسب عدد الأسطر
    def line_number_area_width(self) -> int:
        digits = max(2, len(str(max(1, self.blockCount()))))
        return 16 + self.fontMetrics().horizontalAdvance("9") * digits

    def _update_width(self):
        # هامش على الجانب الأيمن من منفذ العرض
        self.setViewportMargins(0, 0, self.line_number_area_width(), 0)

    def _on_update(self, rect, dy):
        if dy:
            self._gutter.scroll(0, dy)
        else:
            self._gutter.update(0, rect.y(), self._gutter.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_width()

    def resizeEvent(self, event):  # noqa: N802
        super().resizeEvent(event)
        cr = self.contentsRect()
        w = self.line_number_area_width()
        self._gutter.setGeometry(QRect(cr.right() - w + 1, cr.top(), w, cr.height()))

    def paint_line_numbers(self, event):
        painter = QPainter(self._gutter)
        painter.fillRect(event.rect(), QColor(GUTTER))
        block = self.firstVisibleBlock()
        number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()
        painter.setPen(QColor(MUTED))
        align = int(Qt.AlignRight | Qt.AlignVCenter)
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.drawText(
                    0, int(top), self._gutter.width() - 8, height,
                    align, str(number + 1),
                )
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            number += 1


# ── النافذة الرئيسية ──────────────────────────────────────────────────
class HassoobQtIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = HassoobEngine()
        self.current_file = None
        self.setWindowTitle("حاسوب عربي — بيئة التطوير المتكاملة")
        self.resize(1040, 700)
        self.setLayoutDirection(Qt.RightToLeft)

        self._build_toolbar()
        self._build_body()
        self._build_statusbar()
        self._apply_styles()

        self.editor.setPlainText(SAMPLE)
        self._println(" أهلًا بك في بيئة حاسوب عربي. اكتب برنامجك ثم اضغط «تشغيل» (F5).", "info")
        self._update_status()
        self._run_diagnostics()

    # ── الأدوات ─────────────────────────────────────────────────────
    def _act(self, text, slot, shortcut=None):
        a = QAction(text, self)
        a.triggered.connect(slot)
        if shortcut:
            a.setShortcut(QKeySequence(shortcut))
        return a

    def _build_toolbar(self):
        tb = QToolBar("الرئيسية")
        tb.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, tb)
        tb.addAction(self._act("▶ تشغيل", self.run_code, "F5"))
        tb.addAction(self._act("جديد", self.new_file, "Ctrl+N"))
        tb.addAction(self._act("فتح", self.open_file, "Ctrl+O"))
        tb.addAction(self._act("حفظ", self.save_file, "Ctrl+S"))
        tb.addAction(self._act("حفظ باسم", self.save_file_as, "Ctrl+Shift+S"))
        tb.addSeparator()
        tb.addAction(self._act("مسح الخرج", self.clear_output))
        tb.addAction(self._act("جلسة جديدة", self.reset_session))
        tb.addAction(self._act("الدوال", self.show_builtins))
        tb.addAction(self._act("مساعدة", self.show_about))
        # تشغيل سطر الطرفية أيضًا بـ Ctrl+R
        self.addAction(self._act("", self.run_code, "Ctrl+R"))

    def _build_body(self):
        split = QSplitter(Qt.Vertical)

        self.editor = CodeEditor()
        self.editor.setFont(_arabic_font(15))
        self.editor.textChanged.connect(self._update_status)
        self.editor.cursorPositionChanged.connect(self._update_status)
        self.highlighter = QtHighlighter(self.editor.document(), self.engine.builtin_names)

        # ── التشخيص الحيّ: تسطير كل ظهور لاسمٍ غير معرّف ───────────────────
        # السبب: المُحلِّل الدلالي يُبلّغ عن الاسم غير المعرّف مرّةً واحدةً لكل نطاق
        # (الخيار ١، كي لا نُغرق المستخدم بآلاف الأخطاء لجذرٍ واحد). لكنّنا لا نريد
        # أن يخسر بقيّة المواضع، فنرسم تحت *كل* ظهورٍ تسطيرًا مموّجًا أحمر عبر
        # setExtraSelections — والقائمة (شريط الحالة) تبقى رسالةً واحدةً + (+ن).
        # نُعيد الحساب بعد توقّف الكتابة بقليل (debounce) كي لا نُثقل المحرّر.
        self._diag_timer = QTimer(self)
        self._diag_timer.setSingleShot(True)
        self._diag_timer.setInterval(250)
        self._diag_timer.timeout.connect(self._run_diagnostics)
        self.editor.textChanged.connect(self._schedule_diagnostics)
        split.addWidget(self.editor)

        bottom = QWidget()
        v = QVBoxLayout(bottom)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(_arabic_font(13))
        _apply_rtl_text(self.output)
        v.addWidget(self.output, 1)

        repl_row = QWidget()
        h = QHBoxLayout(repl_row)
        h.setContentsMargins(8, 4, 8, 6)
        prompt = QLabel("‹حع›")
        prompt.setStyleSheet(f"color:{ACCENT}; font-weight:bold;")
        self.repl = QLineEdit()
        self.repl.setLayoutDirection(Qt.RightToLeft)
        self.repl.setAlignment(Qt.AlignRight)
        self.repl.setFont(_arabic_font(13))
        self.repl.setPlaceholderText("اكتب تعبيرًا ثم اضغط Enter…")
        self.repl.returnPressed.connect(self._on_repl_enter)
        # في تخطيط يمينيّ، أضِف الموجّه أولًا ليظهر على اليمين.
        h.addWidget(prompt)
        h.addWidget(self.repl, 1)
        v.addWidget(repl_row)

        split.addWidget(bottom)
        split.setSizes([430, 250])
        self.setCentralWidget(split)

    def _build_statusbar(self):
        self.status = self.statusBar()
        # رسالة التشخيص (يسار): أوّل خطأ + عدد البقيّة (+ن) دون إغراق المستخدم.
        self._diag_label = QLabel("")
        self.status.addWidget(self._diag_label)
        self._status_label = QLabel("")
        self.status.addPermanentWidget(self._status_label)

    def _apply_styles(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background:{BG}; color:{FG}; }}
            QPlainTextEdit {{ background:{BG}; color:{FG}; border:none;
                              selection-background-color:#3b3f5c; }}
            QPlainTextEdit#output {{ background:{BG_ALT}; }}
            QLineEdit {{ background:{BG_ALT}; color:{FG}; border:1px solid #3b3f5c;
                         border-radius:6px; padding:5px 8px; }}
            QToolBar {{ background:{BG_ALT}; border:none; spacing:4px; padding:4px; }}
            QToolButton {{ color:{FG}; padding:5px 10px; border-radius:6px; }}
            QToolButton:hover {{ background:{ACCENT}; color:#1b1b27; }}
            QStatusBar {{ background:{BG_ALT}; color:{MUTED}; }}
            QSplitter::handle {{ background:{GUTTER}; }}
        """)
        self.output.setObjectName("output")

    # ── الخرج ───────────────────────────────────────────────────────
    def _emit(self, text, kind="out"):
        color = OUT_COLORS.get(kind, FG)
        safe = _html.escape(text).replace("\n", "<br>").replace(" ", "&nbsp;")
        self.output.appendHtml(f'<span style="color:{color};">{safe}</span>')
        self.output.moveCursor(QTextCursor.End)

    def _print(self, text, kind="out"):
        self._emit(text, kind)

    def _println(self, text, kind="out"):
        self._emit(text + "\n", kind)

    def clear_output(self):
        self.output.clear()

    def reset_session(self):
        self.engine.reset()
        self._println("♻️ بدأت جلسة جديدة (مُسحت كل المتغيّرات والدوال).", "info")

    # ── التشغيل ─────────────────────────────────────────────────────
    def _show_result(self, res):
        if res.output:
            self._emit(res.output, "out")
        if res.value is not None:
            self._println("← " + res.value, "value")
        if not res.ok and res.error:
            self._println(res.error, "err")

    def run_code(self):
        src = self.editor.toPlainText()
        self._println("▶ تشغيل البرنامج", "info")
        res = self.engine.run_source(src, fresh=True)
        self._show_result(res)
        self._update_status()
        self._run_diagnostics()

    # ── التشخيص الحيّ (تسطير كل ظهور لاسمٍ غير معرّف) ────────────────
    def _schedule_diagnostics(self):
        """أعِد جدولة حساب التشخيص بعد توقّف الكتابة (debounce)."""
        self._diag_timer.start()

    def _run_diagnostics(self):
        """حلّل المصدر دون تشغيله وارسم تسطيرًا أحمر تحت *كل* ظهور لاسمٍ غير
        معرّف. يُبلَّغ عن الاسم مرّةً واحدةً لكل نطاق في شريط الحالة (الخيار ١)،
        أمّا التسطير فيشمل جميع المواضع كي يجدها المستخدم بسهولة في ملفٍ طويل.
        تُحسب الإزاحات على نصّ المحرّر نفسه فتنطبق تمامًا على مواضع المستند."""
        source = self.editor.toPlainText()
        try:
            report = self.engine.diagnose(source)
        except Exception:
            report = None

        selections = []
        if report is not None and getattr(report, "underlines", None):
            fmt = QTextCharFormat()
            fmt.setUnderlineStyle(QTextCharFormat.WaveUnderline)
            fmt.setUnderlineColor(QColor("#ff6b6b"))
            fmt.setForeground(QColor("#ff6b6b"))
            doc = self.editor.document()
            n = len(source)
            for u in report.underlines:
                start, end = max(0, u.start), min(n, u.end)
                if end <= start:
                    continue
                cur = QTextCursor(doc)
                cur.setPosition(start)
                cur.setPosition(end, QTextCursor.KeepAnchor)
                sel = QTextEdit.ExtraSelection()
                sel.cursor = cur
                sel.format = fmt
                selections.append(sel)
        self.editor.setExtraSelections(selections)

        diags = report.diagnostics if report is not None else []
        if diags:
            extra = f"  (+{len(diags) - 1})" if len(diags) > 1 else ""
            self._diag_label.setText(f"\u26a0 {diags[0].message}{extra}")
            self._diag_label.setStyleSheet("color:#ff6b6b;")
        else:
            self._diag_label.setText("")
            self._diag_label.setStyleSheet(f"color:{MUTED};")

    def _on_repl_enter(self):
        line = self.repl.text().strip()
        if not line:
            return
        self._println("‹حع› " + line, "repl")
        self.repl.clear()
        res = self.engine.eval_line(line)
        self._show_result(res)

    # ── الملفات ─────────────────────────────────────────────────────
    def new_file(self):
        self.editor.clear()
        self.current_file = None
        self._update_status()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "فتح ملف", "",
            f"ملفات حاسوب عربي (*{EXT});;كل الملفات (*.*)",
        )
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as fh:
                self.editor.setPlainText(fh.read())
            self.current_file = path
            self._println(f"📂 فُتح: {path}", "info")
        except Exception as exc:
            QMessageBox.critical(self, "تعذّر الفتح", str(exc))
        self._update_status()

    def save_file(self):
        if not self.current_file:
            return self.save_file_as()
        self._write(self.current_file)

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "حفظ باسم", "",
            f"ملفات حاسوب عربي (*{EXT});;كل الملفات (*.*)",
        )
        if not path:
            return
        if "." not in os.path.basename(path):
            path += EXT
        self._write(path)

    def _write(self, path):
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(self.editor.toPlainText())
            self.current_file = path
            self._println(f"💾 حُفظ: {path}", "info")
        except Exception as exc:
            QMessageBox.critical(self, "تعذّر الحفظ", str(exc))
        self._update_status()

    # ── حوارات ──────────────────────────────────────────────────────
    def show_builtins(self):
        names = "، ".join(self.engine.builtin_names)
        QMessageBox.information(self, "الدوال المُضمَّنة", names)

    def show_about(self):
        QMessageBox.information(
            self, "حول حاسوب عربي",
            "حاسوب عربي \n"
            "لغة برمجة عربية مستوحاة من Mathematica.\n\n"
            "• اكتب البرنامج ثم اضغط «تشغيل» (F5).\n"
            "• استخدم الطرفية بالأسفل لتجربة التعابير سطرًا سطرًا.\n"
            "• دوال الرسم تفتح نافذة Matplotlib مستقلّة (حفظ/تكبير/تصغير).",
        )

    # ── الحالة ──────────────────────────────────────────────────────
    def _update_status(self):
        cur = self.editor.textCursor()
        line = cur.blockNumber() + 1
        col = cur.positionInBlock() + 1
        name = self.current_file or "بدون عنوان"
        self._status_label.setText(f"{name}   •   السطر {line}، العمود {col}")


def launch():
    """تشغيل واجهة Qt اليمينية. تُعيد رمز الخروج."""
    app = QApplication.instance() or QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    win = HassoobQtIDE()
    win.show()
    return app.exec()
