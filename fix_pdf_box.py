import re

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'r') as f:
    text = f.read()

# Change boxRect to end at endX + 8f and start at summaryX - 8f
text = text.replace("val boxRect = android.graphics.RectF(summaryX - 12f, y, endX + 12f, y + boxHeight)", "val boxRect = android.graphics.RectF(summaryX - 8f, y, endX + 8f, y + boxHeight)")

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'w') as f:
    f.write(text)

