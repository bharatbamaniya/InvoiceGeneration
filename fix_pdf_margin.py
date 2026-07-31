import re

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'r') as f:
    text = f.read()

text = text.replace("val margin = 40f", "val margin = 30f")

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'w') as f:
    f.write(text)

