import re

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'r') as f:
    text = f.read()

start_marker = "fun createPdfInvoice(context: Context, invoice: Invoice): File? {"
end_marker = "fun getPdfUri(context: Context, pdfFile: File): Uri {"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_pdf = """fun createPdfInvoice(context: Context, invoice: Invoice): File? {
        val pdfDocument = PdfDocument()
        
        fun formatCurrency(amount: Double): String {
            val format = java.text.NumberFormat.getNumberInstance(Locale.US)
            format.minimumFractionDigits = 0
            format.maximumFractionDigits = 2
            return format.format(amount)
        }
        
        val baseHeight = 1300f
        val itemHeight = 80f
        val totalHeight = (baseHeight + (invoice.items.size * itemHeight)).toInt()
        val pageWidth = 1200
        val pageInfo = PdfDocument.PageInfo.Builder(pageWidth, totalHeight, 1).create()
        val page = pdfDocument.startPage(pageInfo)
        val canvas = page.canvas

        // Colors
        val pageBgColor = Color.rgb(243, 244, 246)
        val cardBgColor = Color.WHITE
        val primaryColor = Color.rgb(80, 94, 161) // #505EA1
        val textDark = Color.rgb(31, 41, 55) // #1F2937
        val textGray = Color.rgb(75, 85, 99) // #4B5563
        val dividerColor = Color.rgb(229, 231, 235) // #E5E7EB
        val redColor = Color.rgb(220, 38, 38) // #DC2626
        val greenColor = Color.rgb(22, 163, 74) // #16A34A
        val balanceBoxBg = Color.rgb(220, 228, 247) // #DCE4F7

        canvas.drawColor(pageBgColor)

        // Shadow effect
        val shadowPaint = Paint().apply {
            color = Color.argb(10, 0, 0, 0)
            isAntiAlias = true
        }
        for (i in 1..5) {
            val shadowRect = android.graphics.RectF(
                80f - i, 80f - i + 5, 
                pageWidth - 80f + i, totalHeight - 80f + i + 5
            )
            canvas.drawRoundRect(shadowRect, 24f, 24f, shadowPaint)
        }

        val cardPaint = Paint().apply {
            color = cardBgColor
            isAntiAlias = true
        }
        val cardRect = android.graphics.RectF(80f, 80f, pageWidth - 80f.toFloat(), totalHeight - 80f.toFloat())
        canvas.drawRoundRect(cardRect, 24f, 24f, cardPaint)

        val cardBorderPaint = Paint().apply {
            color = dividerColor
            style = Paint.Style.STROKE
            strokeWidth = 2f
            isAntiAlias = true
        }
        canvas.drawRoundRect(cardRect, 24f, 24f, cardBorderPaint)

        // Paints
        val titlePaint = Paint().apply {
            color = primaryColor
            isAntiAlias = true
            textSize = 68f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            textAlign = Paint.Align.CENTER
        }
        
        val addressPaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 22f
            textAlign = Paint.Align.CENTER
        }

        val labelPaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 20f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.NORMAL)
        }

        val namePaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 34f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
        }

        val phonePaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 22f
        }

        val invNoPaint = Paint().apply {
            color = primaryColor
            isAntiAlias = true
            textSize = 42f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            textAlign = Paint.Align.RIGHT
        }

        val datePaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 26f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.NORMAL)
            textAlign = Paint.Align.RIGHT
        }

        val tableHeaderPaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 20f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.NORMAL)
        }

        val tableItemPaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 24f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.NORMAL)
        }
        
        val tableItemMonospacePaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 24f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.NORMAL)
        }
        
        val linePaint = Paint().apply { 
            color = dividerColor
            strokeWidth = 2f 
        }

        val startX = 160f
        val endX = pageWidth - 160f
        val colQtyX = 580f
        val colRateX = 780f
        val centerX = pageWidth / 2f
        
        var y = 200f

        // Header
        canvas.drawText(invoice.storeName, centerX, y, titlePaint)
        y += 50f
        
        if (invoice.storeAddress.isNotBlank()) {
            canvas.drawText(invoice.storeAddress, centerX, y, addressPaint)
            y += 35f
        }
        if (invoice.storePhone.isNotBlank()) {
            canvas.drawText(invoice.storePhone, centerX, y, addressPaint)
            y += 70f
        }

        // Billed To & Invoice details
        val dateFormat = SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
        val dateStr = dateFormat.format(Date(invoice.dateMillis))
        val custName = if (invoice.customerName.isBlank()) "Valued Customer" else invoice.customerName

        canvas.drawText("BILLED TO", startX, y, labelPaint)
        canvas.drawText("INV-${invoice.invoiceId.takeLast(4).padStart(4, '0')}", endX, y, invNoPaint)
        y += 50f
        
        canvas.drawText(custName, startX, y, namePaint)
        canvas.drawText(dateStr, endX, y - 5f, datePaint)
        y += 45f
        
        if (invoice.customerPhone.isNotBlank()) {
            canvas.drawText("Phone: ${invoice.customerPhone}", startX, y, phonePaint)
        }
        y += 70f

        // Table Header
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 50f
        canvas.drawText("ITEM", startX, y, tableHeaderPaint)
        canvas.drawText("QTY", colQtyX, y, Paint(tableHeaderPaint).apply { textAlign = Paint.Align.RIGHT })
        canvas.drawText("RATE (${invoice.currencySymbol})", colRateX, y, Paint(tableHeaderPaint).apply { textAlign = Paint.Align.RIGHT })
        canvas.drawText("AMOUNT (${invoice.currencySymbol})", endX, y, Paint(tableHeaderPaint).apply { textAlign = Paint.Align.RIGHT })
        y += 30f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 70f

        // Table Items
        invoice.items.forEach { item ->
            canvas.drawText(item.item.name, startX, y, tableItemPaint)
            
            val qtyStr = if (item.item.unit == "kg") {
                if (item.quantity % 1.0 == 0.0) "${item.quantity.toInt()} kg" else "${item.quantity} kg"
            } else {
                if (item.quantity % 1.0 == 0.0) "${item.quantity.toInt()} ${item.item.unit}" else "${item.quantity} ${item.item.unit}"
            }
            
            canvas.drawText(qtyStr, colQtyX, y, Paint(tableItemMonospacePaint).apply { textAlign = Paint.Align.RIGHT })
            
            canvas.drawText(formatCurrency(item.unitPrice), colRateX, y, Paint(tableItemMonospacePaint).apply { textAlign = Paint.Align.RIGHT })
            
            canvas.drawText(formatCurrency(item.totalPrice), endX, y, Paint(tableItemMonospacePaint).apply { textAlign = Paint.Align.RIGHT })
            y += itemHeight
        }
        
        y += 20f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 70f

        // Summary
        val summaryLabelPaint = Paint(tableItemPaint).apply { color = textGray }
        val summaryValuePaint = Paint(tableItemPaint).apply { typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
        
        val summaryX = colRateX - 100f
        
        canvas.drawText("Bill Amount", summaryX, y, summaryLabelPaint)
        canvas.drawText("${invoice.currencySymbol}${formatCurrency(invoice.billAmount)}", endX, y, summaryValuePaint)
        y += 60f
        
        if (invoice.previousOutstanding > 0) {
            canvas.drawText("Prev. Outstanding", summaryX, y, summaryLabelPaint)
            canvas.drawText("${invoice.currencySymbol}${formatCurrency(invoice.previousOutstanding)}", endX, y, Paint(summaryValuePaint).apply { color = redColor })
            y += 60f
        }
        
        if (invoice.cashReceived > 0) {
            canvas.drawText("Cash Received", summaryX, y, summaryLabelPaint)
            canvas.drawText("-${invoice.currencySymbol}${formatCurrency(invoice.cashReceived)}", endX, y, Paint(summaryValuePaint).apply { color = greenColor })
            y += 60f
        }
        
        // Total Balance Box
        y += 20f
        val boxHeight = 120f
        val boxRect = android.graphics.RectF(summaryX - 40f, y, endX + 40f, y + boxHeight)
        val boxPaint = Paint().apply {
            color = balanceBoxBg
            isAntiAlias = true
        }
        canvas.drawRoundRect(boxRect, 24f, 24f, boxPaint)
        
        val boxBorderPaint = Paint().apply {
            color = Color.rgb(200, 210, 235)
            style = Paint.Style.STROKE
            strokeWidth = 2f
            isAntiAlias = true
        }
        canvas.drawRoundRect(boxRect, 24f, 24f, boxBorderPaint)
        
        val totalLabelPaint = Paint().apply {
            color = textDark
            textSize = 34f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }
        val totalValPaint = Paint(totalLabelPaint).apply { 
            color = primaryColor
            textSize = 48f
            textAlign = Paint.Align.RIGHT
        }
        
        val totalY = y + (boxHeight / 2) + 14f
        canvas.drawText("Total Balance", summaryX, totalY, totalLabelPaint)
        canvas.drawText("${invoice.currencySymbol}${formatCurrency(invoice.totalBalance)}", endX, totalY, totalValPaint)
        
        y += boxHeight + 80f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 80f
        
        // Footer
        val thankYouPaint = Paint().apply {
            color = primaryColor
            textSize = 28f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.NORMAL)
            isAntiAlias = true
        }
        val sigNamePaint = Paint().apply {
            color = textDark
            textSize = 26f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            textAlign = Paint.Align.RIGHT
            isAntiAlias = true
        }
        val sigTitlePaint = Paint(sigNamePaint).apply {
            textSize = 20f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.NORMAL)
            color = textGray
        }
        
        canvas.drawText("Thank you for shopping with us!", startX, y, thankYouPaint)
        
        canvas.drawText(invoice.storeName, endX, y - 20f, sigNamePaint)
        canvas.drawText("Authorized Signatory", endX, y + 10f, sigTitlePaint)
        
        // Bottom Text
        val bottomPaint = Paint().apply {
            color = textGray
            textSize = 18f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.ITALIC)
            textAlign = Paint.Align.CENTER
            isAntiAlias = true
        }
        canvas.drawText("This is a computer-generated invoice, does not require a physical signature", centerX, totalHeight - 120f, bottomPaint)

        pdfDocument.finishPage(page)

        try {
            val pdfFile = File(context.cacheDir, "Invoice_${invoice.invoiceId}.pdf")
            pdfDocument.writeTo(FileOutputStream(pdfFile))
            pdfDocument.close()
            return pdfFile
        } catch (e: Exception) {
            e.printStackTrace()
            pdfDocument.close()
            return null
        }
    }
    
    """
    
    text = text[:start_idx] + new_pdf + text[end_idx:]
    with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'w') as f:
        f.write(text)

