import re

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'r') as f:
    text = f.read()

old_qty = """        // --- Table Items ---
        invoice.items.forEach { item ->
            canvas.drawText(item.item.name, startX, y, tableItemPaint)
            
            val qtyStr = if (item.item.unit == "kg") {
                if (item.quantity % 1.0 == 0.0) "${item.quantity.toInt()} kg" else "${item.quantity} kg"
            } else {
                if (item.quantity % 1.0 == 0.0) "${item.quantity.toInt()} ${item.item.unit}" else "${item.quantity} ${item.item.unit}"
            }
            
            canvas.drawText(qtyStr, colQtyX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            canvas.drawText(formatCurrency(item.unitPrice), colRateX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            canvas.drawText(formatCurrency(item.totalPrice), endX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            
            y += 24f
        }"""

new_qty = """        // --- Table Items ---
        val sym = invoice.currencySymbol
        invoice.items.forEach { item ->
            canvas.drawText(item.item.name, startX, y, tableItemPaint)
            
            val qtyStr = if (item.quantity % 1.0 == 0.0) "${item.quantity.toInt()}" else "${item.quantity}"
            val rateStr = "$sym${formatCurrency(item.unitPrice)}/${item.item.unit}"
            
            canvas.drawText(qtyStr, colQtyX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            canvas.drawText(rateStr, colRateX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            canvas.drawText(formatCurrency(item.totalPrice), endX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            
            y += 24f
        }"""

text = text.replace(old_qty, new_qty)

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'w') as f:
    f.write(text)
