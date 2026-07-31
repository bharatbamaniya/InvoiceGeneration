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

        // Dark Theme Colors
        val bgColor = Color.rgb(23, 23, 25) // #171719
        val titleColor = Color.rgb(180, 198, 252) // #B4C6FC
        val textLightGray = Color.rgb(161, 161, 170) // #A1A1AA
        val textWhite = Color.WHITE
        val dividerColor = Color.rgb(39, 39, 42) // #27272A
        val redColor = Color.rgb(252, 165, 165) // #FCA5A5
        val balanceBoxColor = Color.rgb(63, 63, 90) // #3F3F5A

        // Fill background
        canvas.drawColor(bgColor)

        // Draw faint grid (optional, but looks nice in reference)
        val gridPaint = Paint().apply {
            color = Color.rgb(32, 32, 35)
            strokeWidth = 1f
        }
        for (i in 0..pageWidth step 40) {
            canvas.drawLine(i.toFloat(), 0f, i.toFloat(), totalHeight.toFloat(), gridPaint)
        }
        for (i in 0..totalHeight step 40) {
            canvas.drawLine(0f, i.toFloat(), pageWidth.toFloat(), i.toFloat(), gridPaint)
        }

        // Draw inner container (darker gray rounded rect)
        val containerPaint = Paint().apply {
            color = Color.rgb(28, 28, 30)
            isAntiAlias = true
        }
        val containerRect = android.graphics.RectF(40f, 40f, pageWidth - 40f.toFloat(), totalHeight - 40f.toFloat())
        canvas.drawRoundRect(containerRect, 20f, 20f, containerPaint)

        // Paints
        val titlePaint = Paint().apply {
            color = titleColor
            isAntiAlias = true
            textSize = 60f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            textAlign = Paint.Align.CENTER
        }
        
        val addressPaint = Paint().apply {
            color = textLightGray
            isAntiAlias = true
            textSize = 20f
            textAlign = Paint.Align.CENTER
        }

        val labelPaint = Paint().apply {
            color = textLightGray
            isAntiAlias = true
            textSize = 18f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
        }

        val namePaint = Paint().apply {
            color = textWhite
            isAntiAlias = true
            textSize = 30f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
        }

        val phonePaint = Paint().apply {
            color = textLightGray
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
            color = textWhite
            isAntiAlias = true
            textSize = 24f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            textAlign = Paint.Align.RIGHT
        }

        val tableHeaderPaint = Paint().apply {
            color = textLightGray
            isAntiAlias = true
            textSize = 18f
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.BOLD)
        }

        val tableItemPaint = Paint().apply {
            color = textWhite
            isAntiAlias = true
            textSize = 22f
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
            
            canvas.drawText(qtyStr, colQtyX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            
            val rateStr = if (item.unitPrice % 1.0 == 0.0) "${item.unitPrice.toInt()}" else String.format(Locale.US, "%.2f", item.unitPrice)
            canvas.drawText(rateStr, colRateX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            
            val amtStr = if (item.totalPrice % 1.0 == 0.0) "${item.totalPrice.toInt()}" else String.format(Locale.US, "%.2f", item.totalPrice)
            canvas.drawText(amtStr, endX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            y += itemHeight
        }
        
        y += 20f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 60f

        // Summary
        val summaryLabelPaint = Paint(tableItemPaint).apply { color = textLightGray }
        val summaryValuePaint = Paint(tableItemPaint).apply { typeface = Typeface.create(Typeface.MONOSPACE, Typeface.BOLD) }
        
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
            canvas.drawText("-${invoice.currencySymbol}$cashStr", endX, y, Paint(summaryValuePaint).apply { color = Color.rgb(134, 239, 172) })
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
        
        val totalLabelPaint = Paint().apply {
            color = textWhite
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
        canvas.drawText("${invoice.currencySymbol}$totStr", endX, totalY, totalValPaint)
        
        y += boxHeight + 80f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 60f
        
        // Footer
        val thankYouPaint = Paint().apply {
            color = textWhite
            textSize = 24f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }
        val sigNamePaint = Paint().apply {
            color = textLightGray
            textSize = 20f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            textAlign = Paint.Align.RIGHT
            isAntiAlias = true
        }
        val sigTitlePaint = Paint(sigNamePaint).apply {
            textSize = 16f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.NORMAL)
        }
        
        canvas.drawText("Thank you for shopping with us!", startX, y, thankYouPaint)
        
        canvas.drawText(invoice.storeName, endX, y - 20f, sigNamePaint)
        canvas.drawText("Authorized Signatory", endX, y + 5f, sigTitlePaint)
        
        // Bottom Text
        val bottomPaint = Paint().apply {
            color = Color.rgb(113, 113, 122) // #71717A
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

