# حاسوب عربي (Hāssoob ʻArabī)

لغة برمجة عربية كاملة مستوحاة من Wolfram Mathematica — تدعم الحساب الرمزي
والعددي والرسم البياني مع بنية لغوية عربية بالكامل.

A complete Arabic programming language inspired by Wolfram Mathematica:
symbolic + numeric computation, plotting, and fully Arabic syntax.

## بنية المشروع / Project layout

```
HassoobArabi/
├─ HassoobArabi.g4        قواعد ANTLR4 (grammar)
├─ generated/             مخرجات ANTLR4 (تُولّد — انظر أدناه)
├─ ide/                   بيئة التطوير الرسومية (RTL)
│  ├─ engine.py           محرّك التنفيذ/REPL (بلا اعتماد على واجهة)
│  ├─ highlight.py        مُلوّن البنية (بلا اعتماد على واجهة)
│  └─ editor.py           واجهة Tkinter اليمينية
├─ src/                   الشيفرة المصدرية
│  ├─ ast_nodes.py        عقد الشجرة (مُعطى)
│  ├─ ast_builder.py      باني الشجرة (مُعطى)
│  ├─ errors.py           الأخطاء وإشارات التحكم
│  ├─ environment.py      سلسلة النطاقات
│  ├─ optimizer.py        المُحسّن
│  ├─ semantic.py         المحلل الدلالي
│  ├─ interpreter.py      المُفسّر
│  ├─ builtins.py         الدوال المدمجة
│  ├─ _builtins_loader.py مُحمّل يتجنّب تعارض الاسم مع builtins القياسية
│  └─ repl.py             الصدفة التفاعلية
├─ tests/                 اختبارات pytest
├─ examples/              برامج أمثلة (.حع)
├─ main.py                نقطة الدخول
└─ requirements.txt
```

## التثبيت / Setup

```bash
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
