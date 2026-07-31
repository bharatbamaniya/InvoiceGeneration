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
        
        val baseHeight = 900f
        val itemHeight = 60f
        val totalHeight = (baseHeight + (invoice.items.size * itemHeight)).toInt()
        val pageWidth = 800
        val pageInfo = PdfDocument.PageInfo.Builder(pageWidth, totalHeight, 1).create()
        val page = pdfDocument.startPage(pageInfo)
        val canvas = page.canvas

        // Light Theme Colors
        val bgColor = Color.rgb(248, 249, 250) // Very light gray background
        val containerColor = Color.rgb(243, 244, 246) // Slightly darker than white for the card
        val titleColor = Color.rgb(79, 90, 161) // Indigo/Blue for main title and accents
        val textDark = Color.rgb(31, 41, 55) // Main text color
        val textGray = Color.rgb(107, 114, 128) // Secondary text color
        val dividerColor = Color.rgb(229, 231, 235) // Light gray divider
        val redColor = Color.rgb(220, 38, 38) // Red for outstanding
        val balanceBoxColor = Color.rgb(219, 224, 245) // Light blue box bg

        // Fill background
        canvas.drawColor(bgColor)

        // Draw inner container (light gray rounded rect)
        val containerPaint = Paint().apply {
            color = containerColor
            isAntiAlias = true
        }
        val containerRect = android.graphics.RectF(40f, 40f, pageWidth - 40f.toFloat(), totalHeight - 40f.toFloat())
        canvas.drawRoundRect(containerRect, 20f, 20f, containerPaint)
        
        val containerBorderPaint = Paint().apply {
            color = dividerColor
            style = Paint.Style.STROKE
            strokeWidth = 2f
            isAntiAlias = true
        }
        canvas.drawRoundRect(containerRect, 20f, 20f, containerBorderPaint)

        // Paints
        val titlePaint = Paint().apply {
            color = titleColor
            isAntiAlias = true
            textSize = 60f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            textAlign = Paint.Align.CENTER
        }
        
        val addressPaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 20f
            textAlign = Paint.Align.CENTER
        }

        val labelPaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 18f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.NORMAL)
        }

        val namePaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 30f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
        }

        val phonePaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 22f
        }

        val invNoPaint = Paint().apply {
            color = titleColor
            isAntiAlias = true
            textSize = 36f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            textAlign = Paint.Align.RIGHT
        }

        val datePaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 24f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.NORMAL)
            textAlign = Paint.Align.RIGHT
        }

        val tableHeaderPaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 18f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.NORMAL)
        }

        val tableItemPaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 22f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.NORMAL)
        }
        
        val tableItemMonospacePaint = Paint().apply {
            color = textDark
            isAntiAlias = true
            textSize = 20f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.NORMAL)
        }
        
        val linePaint = Paint().apply { 
            color = dividerColor
            strokeWidth = 2f 
        }

        val startX = 80f
        val colQtyX = 400f
        val colRateX = 550f
        val endX = pageWidth - 80f
        val centerX = pageWidth / 2f
        
        var y = 140f

        // Title
        canvas.drawText(invoice.storeName, centerX, y, titlePaint)
        y += 40f
        
        if (invoice.storeAddress.isNotBlank()) {
            canvas.drawText(invoice.storeAddress, centerX, y, addressPaint)
            y += 30f
        }
        if (invoice.storePhone.isNotBlank()) {
            canvas.drawText(invoice.storePhone, centerX, y, addressPaint)
            y += 60f
        }

        // Billed To & Invoice details
        val dateFormat = SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
        val dateStr = dateFormat.format(Date(invoice.dateMillis))
        val custName = if (invoice.customerName.isBlank()) "Valued Customer" else invoice.customerName

        canvas.drawText("BILLED TO", startX, y, labelPaint)
        canvas.drawText("INV-${invoice.invoiceId.takeLast(4)}", endX, y, invNoPaint)
        y += 40f
        
        canvas.drawText(custName, startX, y, namePaint)
        canvas.drawText(dateStr, endX, y, datePaint)
        y += 40f
        
        if (invoice.customerPhone.isNotBlank()) {
            canvas.drawText("📞 ${invoice.customerPhone}", startX, y, phonePaint)
        }
        y += 60f

        // Table Header
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 40f
        canvas.drawText("ITEM", startX, y, tableHeaderPaint)
        canvas.drawText("QTY", colQtyX, y, Paint(tableHeaderPaint).apply { textAlign = Paint.Align.RIGHT })
        canvas.drawText("RATE (${invoice.currencySymbol})", colRateX, y, Paint(tableHeaderPaint).apply { textAlign = Paint.Align.RIGHT })
        canvas.drawText("AMOUNT (${invoice.currencySymbol})", endX, y, Paint(tableHeaderPaint).apply { textAlign = Paint.Align.RIGHT })
        y += 20f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 50f

        // Table Items
        invoice.items.forEach { item ->
            canvas.drawText(item.item.name, startX, y, tableItemPaint)
            
            // Format qty depending on unit
            val qtyStr = if (item.item.unit == "kg") {
                if (item.quantity % 1.0 == 0.0) "${item.quantity.toInt()} kg" else "${item.quantity} kg"
            } else {
                if (item.quantity % 1.0 == 0.0) "${item.quantity.toInt()} ${item.item.unit}" else "${item.quantity} ${item.item.unit}"
            }
            
            canvas.drawText(qtyStr, colQtyX, y, Paint(tableItemMonospacePaint).apply { textAlign = Paint.Align.RIGHT })
            
            val rateStr = if (item.unitPrice % 1.0 == 0.0) "${item.unitPrice.toInt()}" else String.format(Locale.US, "%.2f", item.unitPrice)
            canvas.drawText(rateStr, colRateX, y, Paint(tableItemMonospacePaint).apply { textAlign = Paint.Align.RIGHT })
            
            val amtStr = if (item.totalPrice % 1.0 == 0.0) "${item.totalPrice.toInt()}" else String.format(Locale.US, "%.2f", item.totalPrice)
            canvas.drawText(amtStr, endX, y, Paint(tableItemMonospacePaint).apply { textAlign = Paint.Align.RIGHT })
            y += itemHeight
        }
        
        y += 20f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 60f

        // Summary
        val summaryLabelPaint = Paint(tableItemPaint).apply { color = textDark }
        val summaryValuePaint = Paint(tableItemPaint).apply { typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD) }
        
        val summaryX = pageWidth / 2f
        
        val billAmtStr = if (invoice.billAmount % 1.0 == 0.0) "${invoice.billAmount.toInt()}" else String.format(Locale.US, "%.2f", invoice.billAmount)
        canvas.drawText("Bill Amount", summaryX, y, summaryLabelPaint)
        canvas.drawText("${invoice.currencySymbol}$billAmtStr", endX, y, summaryValuePaint)
        y += 50f
        
        if (invoice.previousOutstanding > 0) {
            val prevStr = if (invoice.previousOutstanding % 1.0 == 0.0) "${invoice.previousOutstanding.toInt()}" else String.format(Locale.US, "%.2f", invoice.previousOutstanding)
            canvas.drawText("Prev. Outstanding", summaryX, y, summaryLabelPaint)
            canvas.drawText("${invoice.currencySymbol}$prevStr", endX, y, Paint(summaryValuePaint).apply { color = redColor })
            y += 50f
        }
        
        if (invoice.cashReceived > 0) {
            val cashStr = if (invoice.cashReceived % 1.0 == 0.0) "${invoice.cashReceived.toInt()}" else String.format(Locale.US, "%.2f", invoice.cashReceived)
            canvas.drawText("Cash Received", summaryX, y, summaryLabelPaint)
            canvas.drawText("-${invoice.currencySymbol}$cashStr", endX, y, Paint(summaryValuePaint).apply { color = Color.rgb(22, 163, 74) })
            y += 50f
        }
        
        // Total Balance Box
        y += 20f
        val boxHeight = 100f
        val boxRect = android.graphics.RectF(summaryX - 40f, y, endX + 40f, y + boxHeight)
        val boxPaint = Paint().apply {
            color = balanceBoxColor
            isAntiAlias = true
        }
        canvas.drawRoundRect(boxRect, 20f, 20f, boxPaint)
        
        val boxBorderPaint = Paint().apply {
            color = Color.rgb(180, 190, 225)
            style = Paint.Style.STROKE
            strokeWidth = 2f
            isAntiAlias = true
        }
        canvas.drawRoundRect(boxRect, 20f, 20f, boxBorderPaint)
        
        val totalLabelPaint = Paint().apply {
            color = textDark
            textSize = 30f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }
        val totalValPaint = Paint(totalLabelPaint).apply { 
            color = titleColor
            textSize = 40f
            textAlign = Paint.Align.RIGHT
        }
        
        val totalY = y + (boxHeight / 2) + 12f
        val totStr = if (invoice.totalBalance % 1.0 == 0.0) "${invoice.totalBalance.toInt()}" else String.format(Locale.US, "%.2f", invoice.totalBalance)
        canvas.drawText("Total Balance", summaryX, totalY, totalLabelPaint)
        canvas.drawText("${invoice.currencySymbol}$totStr", endX - 20f, totalY, totalValPaint)
        
        y += boxHeight + 80f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 60f
        
        // Footer
        val thankYouPaint = Paint().apply {
            color = titleColor
            textSize = 24f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.NORMAL)
            isAntiAlias = true
        }
        val sigNamePaint = Paint().apply {
            color = textDark
            textSize = 20f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            textAlign = Paint.Align.RIGHT
            isAntiAlias = true
        }
        val sigTitlePaint = Paint(sigNamePaint).apply {
            textSize = 16f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.NORMAL)
            color = textGray
        }
        
        canvas.drawText("Thank you for shopping with us!", startX, y, thankYouPaint)
        
        canvas.drawText(invoice.storeName, endX, y - 20f, sigNamePaint)
        canvas.drawText("Authorized Signatory", endX, y + 5f, sigTitlePaint)
        
        // Bottom Text
        val bottomPaint = Paint().apply {
            color = textGray
            textSize = 16f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.ITALIC)
            textAlign = Paint.Align.CENTER
            isAntiAlias = true
        }
        canvas.drawText("This is a computer-generated invoice, does not require a physical signature", centerX, totalHeight - 80f, bottomPaint)

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

