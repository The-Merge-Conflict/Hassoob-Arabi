# حاسوب عربي (Hāssoob ʻArabī)

لغة برمجة عربية كاملة مستوحاة من Wolfram Mathematica — تدعم الحساب الرمزي
والعددي والرسم البياني مع بنية لغوية عربية بالكامل.

A complete Arabic programming language inspired by Wolfram Mathematica:
symbolic + numeric computation, plotting, and fully Arabic syntax.

## بنية المشروع / Project layout

```
HassoobArabi/
├─ HassoobArabi.g4         قواعد ANTLR4 (تعريف اللغة)
├─ generated/             المحلل اللفظي/النحوي المولَّد من ANTLR4 (ناتج بناء)
├─ main.py                نقطة الدخول (تشغيل ملف / REPL / -c / --ide)
├─ requirements.txt       اعتماديات بايثون
├─ src/
│  ├─ ast_nodes/          أصناف عقد الـ AST (حزمة)
│  │  ├─ __init__.py        يعيد تصدير كل عقدة (يحافظ على `from ast_nodes import *`)
│  │  ├─ base.py            المزيج _Positioned لموقع المصدر
│  │  ├─ statements.py      عقد الجُمل / التحكم بالتدفق
│  │  ├─ expressions.py     عقد التعابير (العوامل، الاستدعاءات، الفهرسة، اللامبدا)
│  │  └─ literals.py        عقد القيم الحرفية / الثوابت (الأرقام، النصوص، القوائم، π/e/∞)
│  ├─ ast_builder.py      شجرة الإعراب ← AST
│  ├─ semantic.py         التحليل الدلالي الساكن
│  ├─ optimizer.py        مُحسِّن الـ AST
│  ├─ interpreter/        المفسّر الجائب للشجرة (حزمة)
│  │  ├─ __init__.py        يعيد تصدير Interpreter وFunction وparse_program وparse_expression وrun_source
│  │  ├─ evaluator.py       قيمة Function + صنف Interpreter
│  │  ├─ parsing.py         واجهة ANTLR الأمامية + أخطاء نحوية عربية لطيفة
│  │  └─ pipeline.py        run_source: التحليل ← التحسين ← التحليل الدلالي ← التفسير
│  ├─ environment.py      سلسلة النطاقات
│  ├─ library/            المكتبة القياسية (حزمة، تحل محل builtins.py)
│  │  ├─ __init__.py        يجمّع سجلّ BUILTINS من جميع المجالات
│  │  ├─ _shared.py         مساعدات مشتركة (تحويل الأعداد، الكائنات القابلة للاستدعاء، …)
│  │  ├─ formatting.py      تنسيق المخرجات / القيم (format_value، to_arabic_digits)
│  │  ├─ symbolic.py        الرياضيات الرمزية (الاشتقاق، التكامل، الحل، …)
│  │  ├─ numeric.py         العمليات العددية والجبر الخطي
│  │  ├─ statistics.py      الإحصاء
│  │  ├─ text_lists.py      دوال القوائم والنصوص
│  │  └─ plotting.py        الرسم البياني (Matplotlib آمن بلا واجهة)
│  ├─ _builtins_loader.py يحمّل BUILTINS من library/ (يتجنّب التعارض مع builtins القياسية)
│  ├─ runtime_ops.py      مساعدات زمن التشغيل للعوامل / الفهرسة
│  ├─ lang_utils.py       أدوات مشتركة
│  ├─ errors/             التسلسل الهرمي للأخطاء العربية + إشارات التحكم (حزمة)
│  │  ├─ __init__.py        يعيد تصدير كامل الواجهة العامة
│  │  ├─ base.py            to_arabic_digits، closest_name، HassoobError
│  │  ├─ syntax.py          LexError، ParseError
│  │  ├─ semantic.py        SemanticError، MultiError
│  │  ├─ runtime.py         HassoobRuntimeError
│  │  └─ signals.py         ReturnSignal، BreakSignal، ContinueSignal
│  └─ repl.py             الصدفة التفاعلية
├─ ide/
│  ├─ engine.py           محرك تشغيل/REPL مستقل عن الواجهة
│  ├─ highlight.py        مُلوِّن بنيوي مستقل عن الواجهة
│  ├─ editor_qt.py        محرر PySide6 (Qt) يميني الاتجاه — الأساسي
│  ├─ editor.py           محرر Tkinter يميني الاتجاه — بديل بلا تثبيت
│  ├─ __init__.py         يختار Qt تلقائيًا، ويرجع إلى Tkinter عند الحاجة
│  └─ __main__.py         مُشغِّل `python -m ide`
├─ tests/                 مجموعات اختبارات pytest (تبني أشجار AST مباشرة)
└─ examples/              برامج أمثلة (.حع)
```

## التثبيت / Setup

```bash
python -m venv venv
run the activation script for the venv under venv/Scripts/activate
pip install -r requirements.txt

# توليد المحلل من القواعد (يتطلب Java + أداة antlr4)
antlr4 -Dlanguage=Python3 -visitor -o generated HassoobArabi.g4
```

## التشغيل / Usage

```bash
python main.py                  # الصدفة التفاعلية (REPL)
python main.py examples/مرحبا.حع  # تشغيل ملف
 python main.py -c "اطبع(٣+٤)"   # تنفيذ تعبير واحد
python main.py --ide            # فتح بيئة التطوير الرسومية
```

## بيئة التطوير الرسومية / Graphical IDE

بيئة تطوير متكاملة مبنية على Tkinter (تأتي مع بايثون، بلا حزم إضافية):

```bash
python main.py --ide      # أو
python -m ide
```

المميزات:

- 📝 **محرّر يميني (RTL)** مع أرقام أسطر وتلوين للكلمات المفتاحية
  والدوال المدمجة والأرقام والنصوص والتعليقات.
- ▶ **تشغيل فوري** (F5 أو Ctrl+R) مع عرض المخرجات والأخطاء اللطيفة بالعربية.
- ← **طرفيّة (REPL) تفاعلية** بالعربية تشارك حالة الجلسة مع المحرّر.
- 📂 **فتح/حفظ** ملفات `.حع` (دعم UTF-8 الكامل).
- 🔢 كل المخرجات بأرقام عربية ٧، والرسوم البيانية تظهر في نوافذ مستقلة.

> على لينكس قد تحتاج لتثبيت Tkinter: `sudo apt install python3-tk`.
> لأجمل عرض للخط العربي، رُكّب خطًّا مثل Amiri أو Noto Naskh Arabic.
>
> يحتاج التشغيل الفعلي للشيفرة إلى توليد محلّل ANTLR أولاً (انظر «التثبيت»)؛
> وإلّا ستظهر رسالة لطيفة تطلب ذلك.

## الاختبارات / Tests

```bash
pytest tests/
# أو بدون pytest: كل ملف اختبار يعمل مباشرةً
python tests/test_optimizer.py
python tests/test_interpreter.py
python tests/test_builtins.py
python tests/test_ide.py
```

الاختبارات تبني شجرة البناء مباشرةً (دون الحاجة للمحلل المولّد) لذا تعمل حتى قبل توليد ANTLR.

## ملاحظة حول القواعد / Grammar note

تمت مراجعة `HassoobArabi.g4` بالكامل مقابل `ast_builder.py` والمُفسّر؛ لم تكن هناك
حاجة لأي تغيير وظيفي (انظر التعليق في أعلى الملف).
