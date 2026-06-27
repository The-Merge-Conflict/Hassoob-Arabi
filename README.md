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
├─ conftest.py            تهيئة مسارات pytest (تسجّل مجلّدات المراحل قبل الاختبارات)
├─ requirements.txt       اعتماديات بايثون
├─ src/
│  ├─ _pathsetup.py       يسجّل جذر المصدر وكل مجلّدات المراحل على sys.path
│  ├─ frontend/           الواجهة الأمامية — تحليل لفظي/نحوي ← AST
│  │  ├─ parsing.py         واجهة ANTLR + التطبيع (normalization) + أخطاء نحوية عربية لطيفة
│  │  ├─ lang_utils.py      أدوات لفظية مشتركة (فكّ الهروب، النصوص المنسّقة)
│  │  └─ ast_nodes/         أصناف عقد الـ AST (base, statements, expressions, literals)
│  ├─ ast_builder.py      (مُعطى — لا يُعدّل) شجرة الإعراب ← AST؛ يبقى في src/ لمساره الثابت
│  ├─ midend/             الواجهة الوسطى — تحليل دلالي + تحسين
│  │  ├─ semantic.py        تحليل ساكن يجمع كل الأخطاء (لا يتوقف عند أوّل خطأ)
│  │  └─ optimizer.py       مُحسّن الـ AST (طيّ الثوابت، التبسيط، إزالة الفروع الميتة)
│  ├─ backend/            الواجهة الخلفية — تنفيذ + زمن تشغيل
│  │  ├─ evaluator.py       قيمة Function + صنف Interpreter
│  │  ├─ environment.py     سلسلة النطاقات
│  │  ├─ runtime_ops.py     مساعدات زمن التشغيل للعوامل / الفهرسة
│  │  ├─ _builtins_loader.py يحمّل BUILTINS من library/
│  │  └─ library/           المكتبة القياسية (formatting, symbolic, numeric, statistics, text_lists, plotting, _shared)
│  ├─ driver/             الموجّه — يربط المراحل معًا
│  │  ├─ pipeline.py        compile_program / run_source: تحليل ← تحليل دلالي ← تحسين ← تفسير
│  │  └─ repl.py            الصدفة التفاعلية
│  ├─ errors/             تسلسل الأخطاء العربية المشترك + إشارات التحكم (base, syntax, semantic, runtime, signals)
│  └─ interpreter/        واجهة تصدير رفيعة (façade) تُبقي اسم الاستيراد العام مستقرّا
├─ ide/                   محرك مستقل عن الواجهة + محرّرات RTL (Qt أساسي، Tkinter بديل)
├─ tests/                 مجموعات اختبارات (تبني أشجار AST مباشرة)
└─ examples/              برامج أمثلة (.حع)
```

## المعمارية ثلاثية الطبقات / Three-layer architecture

الكود منظّم فيزيائيًّا حسب مرحلة الترجمة لإبراز الواجهات الثلاث بوضوح:

- **الواجهة الأمامية / Front End** (`src/frontend/`) — التطبيع والتحليل اللفظي/النحوي وبناء الـ AST.
- **الواجهة الوسطى / Middle End** (`src/midend/`) — التحليل الدلالي ثم التحسين.
- **الواجهة الخلفية / Back End** (`src/backend/`) — التنفيذ وزمن التشغيل والمكتبة القياسية.

يربطها موجّه صغير (`src/driver/`) بترتيب: **تحليل ← تحليل دلالي ← تحسين ← تفسير**، وتتشارك تسلسل الأخطاء (`src/errors/`). التفاصيل الكاملة — ومعها **دليل المطوّر** (إكمال تطوير اللغة) و**دليل المستخدم** وشرح **معالجة الأخطاء** و**التطبيع (normalization)** — في [التوثيق بالعربية](docs/HassoobArabi_Documentation_AR.md) و[بالإنجليزية](docs/HassoobArabi_Documentation_EN.md).

## التثبيت / Setup

```bash
python -m venv venv
run the activation script for the venv under venv/Scripts/activate
pip install -r requirements.txt
```

### توليد المحلل من القواعد / Generate the parser

أداة ANTLR4 مكتوبة بلغة Java، لذا تحتاج أولًا إلى:

1. **تثبيت Java** (إصدار 11 أو أحدث): <https://www.oracle.com/java/technologies/downloads/> أو
   أي توزيعة OpenJDK مثل <https://adoptium.net/>.
2. **تنزيل أداة ANTLR4 من الموقع الرسمي**: <https://www.antlr.org/download.html>
   — نزّل ملف `antlr-4.13.1-complete.jar` (يطابق إصدار `antlr4-python3-runtime`
   في `requirements.txt`) واحفظه في مكان معروف.
3. **اضبط الأمر `antlr4` كاختصار** لتشغيل ذلك الملف:

```bash
# Linux / macOS — أضف السطرين إلى ~/.bashrc أو ~/.zshrc
export CLASSPATH=".:/path/to/antlr-4.13.1-complete.jar:$CLASSPATH"
alias antlr4='java -jar /path/to/antlr-4.13.1-complete.jar'
```

```powershell
# Windows PowerShell — أو ببساطة استدعِ الملف مباشرةً عبر java -jar
java -jar C:\path\to\antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -o generated HassoobArabi.g4
```

ثم ولّد المحلّل اللفظي/النحوي (يُنشئ مجلّد `generated` تلقائيًا إن لم يكن موجودًا):

```bash
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

---

## ١١. آفاق مستقبلية

> *أفكار للمطوّرين:* يجمع هذا القسم ما يمكن إضافته إلى اللغة مستقبلًا، وما كنّا سنضيفه لو اتّسع الوقت. والبنية ثلاثية الطبقات (أمامية/وسطى/خلفية) تجعل كلّ فكرة منها قابلةً للإضافة في موضعها الطبيعي.

### ١. الأعداد المركّبة (Complex numbers)
دعم الأعداد المركّبة `أ + ب ت` (حيث `ت` الوحدة التخيلية)، مع العمليات الحسابية عليها ودوالّ مرافقة مثل: الجزء الحقيقي، والجزء التخيلي، والمرافق، والمقياس. الإضافة تمسّ الواجهة الخلفية أساسًا: نوع قيمة جديد في `src/backend/`، ودلالات العوامل في `runtime_ops.py`، ودوال في `library/numeric.py`، مع تطبيع رمز الوحدة التخيلية في الواجهة الأمامية.

### ٢. دالة «إلى_تعبير» (تحويل النص إلى تعبير، على غرار `ToExpression` في Mathematica)
دالة تأخذ نصًّا وتعيد قيمته بعد تحليله وتقييمه — لتحويل النصوص إلى أرقام أو حتّى إلى تعابير رمزية كاملة. تُعيد استخدام الواجهة الأمامية الموجودة (`parse_expression`) ثم تمرّ بالتقييم في الخلفية، فلا تحتاج تعديلًا في القواعد.

### ٣. ترجمة كل الأخطاء إلى العربية
نُترجم اليوم معظم أخطاء ANTLR إلى رسائل عربية لطيفة، لكن تبقى حالات تظهر بالإنجليزية (من ANTLR أو من بايثون)، ونطمح لالتقاطها كلّها وصبّها في الصيغة العربية الموحّدة. مثال لم يُترجَم بعد — وضع وسيط موضعي بعد وسيط مُسمّى:

> After the **named** argument عنوان="التوزيع التكراري", you put a **positional** argument 8 (separated by the Arabic comma ،). A positional argument is not allowed to come after a named one.

والهدف رسالة عربية بصيغتنا المعيارية، مثل:

```
خطأ في السطر {رقم}، العمود {رقم}: لا يجوز وضع وسيط موضعي (٨) بعد وسيط مُسمّى (عنوان="التوزيع التكراري").
   ↪ انقل الوسيط الموضعي قبل الوسطاء المُسمّاة.
   💡 رتّب الوسطاء: الموضعية أولًا ثم المُسمّاة.
```

### ٤. امتداد لـ VS Code
امتداد رسمي للغة في Visual Studio Code: تلوين نحوي عبر قواعد TextMate لملفات `.حع`، وإكمال تلقائي للكلمات المفتاحية والدوال المدمجة، وإبراز للأخطاء أثناء الكتابة عبر خادم لغة (LSP) يُعيد استخدام محرّك التشخيص الموجود في `ide/engine.py`، مع دعم الكتابة من اليمين إلى اليسار (RTL).

ونرحّب بإسهامات المطوّرين في أيّ من هذه المحاور.

---