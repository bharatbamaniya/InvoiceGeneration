import re

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'r') as f:
    text = f.read()

old_amt = 'canvas.drawText(formatCurrency(item.totalPrice), endX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })'
new_amt = 'canvas.drawText("$sym${formatCurrency(item.totalPrice)}", endX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })'

text = text.replace(old_amt, new_amt)

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'w') as f:
    f.write(text)
