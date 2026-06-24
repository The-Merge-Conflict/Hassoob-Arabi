هذا المجلد مخصص لمخرجات ANTLR4 (لا تُعدّل يدوياً).
This directory holds the ANTLR4-generated parser. DO NOT edit by hand.

Generate the parser (requires Java + the antlr4 tool) from the project root:

    antlr4 -Dlanguage=Python3 -visitor -o generated HassoobArabi.g4

or, using the jar directly:

    java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -o generated HassoobArabi.g4

After generation this directory should contain:
    HassoobArabiLexer.py
    HassoobArabiParser.py
    HassoobArabiVisitor.py
    HassoobArabiListener.py
