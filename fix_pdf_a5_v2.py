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
        
        val pageWidth = 420 // ISO A5 width in points
        var estimatedHeight = 480f + (invoice.items.size * 25f)
        val totalHeight = Math.max(595, estimatedHeight.toInt()) // ISO A5 height is 595
        
        val pageInfo = PdfDocument.PageInfo.Builder(pageWidth, totalHeight, 1).create()
        val page = pdfDocument.startPage(pageInfo)
        val canvas = page.canvas

        // Colors
        val pageBgColor = Color.WHITE
        val primaryColor = Color.rgb(79, 70, 229) // Indigo-600 #4F46E5
        val primaryLight = Color.rgb(238, 242, 255) // Indigo-50
        val textDark = Color.rgb(17, 24, 39) // Gray-900
        val textGray = Color.rgb(107, 114, 128) // Gray-500
        val textLight = Color.rgb(156, 163, 175) // Gray-400
        val dividerColor = Color.rgb(229, 231, 235) // Gray-200
        
        canvas.drawColor(pageBgColor)

        // Typefaces
        val sansSerif = Typeface.create("sans-serif", Typeface.NORMAL)
        val sansSerifMedium = Typeface.create("sans-serif-medium", Typeface.NORMAL)
        val sansSerifBold = Typeface.create("sans-serif", Typeface.BOLD)

        val titlePaint = Paint().apply {
            color = primaryColor
            textSize = 28f
            typeface = sansSerifBold
            textAlign = Paint.Align.CENTER
            isAntiAlias = true
        }
        
        val subtitlePaint = Paint().apply {
            color = textDark
            textSize = 10f
            typeface = sansSerifMedium
            textAlign = Paint.Align.CENTER
            isAntiAlias = true
        }
        
        val addressPaint = Paint().apply {
            color = textGray
            textSize = 9f
            typeface = sansSerif
            textAlign = Paint.Align.CENTER
            isAntiAlias = true
        }

        val labelPaint = Paint().apply {
            color = textLight
            textSize = 8f
            typeface = sansSerifMedium
            letterSpacing = 0.05f
            isAntiAlias = true
        }

        val namePaint = Paint().apply {
            color = textDark
            textSize = 14f
            typeface = sansSerifBold
            isAntiAlias = true
        }

        val invNoPaint = Paint().apply {
            color = primaryColor
            textSize = 14f
            typeface = sansSerifMedium
            textAlign = Paint.Align.RIGHT
            isAntiAlias = true
        }

        val datePaint = Paint().apply {
            color = textDark
            textSize = 10f
            typeface = sansSerifMedium
            textAlign = Paint.Align.RIGHT
            isAntiAlias = true
        }

        val tableHeaderPaint = Paint().apply {
            color = textGray
            textSize = 9f
            typeface = sansSerifMedium
            letterSpacing = 0.05f
            isAntiAlias = true
        }

        val tableItemPaint = Paint().apply {
            color = textDark
            textSize = 10f
            typeface = sansSerif
            isAntiAlias = true
        }
        
        val linePaint = Paint().apply { 
            color = dividerColor
            strokeWidth = 1f 
        }

        val margin = 40f
        val startX = margin
        val endX = pageWidth - margin
        val centerX = pageWidth / 2f
        
        val colQtyX = 220f
        val colRateX = 300f
        
        var y = 50f

        // --- Header ---
        canvas.drawText(invoice.storeName, centerX, y, titlePaint)
        y += 18f
        
        if (invoice.storeSubtitle.isNotBlank()) {
            canvas.drawText(invoice.storeSubtitle, centerX, y, subtitlePaint)
            y += 14f
        }
        if (invoice.storeAddress.isNotBlank()) {
            canvas.drawText(invoice.storeAddress, centerX, y, addressPaint)
            y += 12f
        }
        if (invoice.storePhone.isNotBlank()) {
            canvas.drawText(invoice.storePhone, centerX, y, addressPaint)
            y += 20f
        } else {
            y += 8f
        }

        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 20f

        // --- Billed To & Invoice details ---
        val dateFormat = SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
        val dateStr = dateFormat.format(Date(invoice.dateMillis))
        val custName = if (invoice.customerName.isBlank()) "Valued Customer" else invoice.customerName

        canvas.drawText("BILLED TO", startX, y, labelPaint)
        canvas.drawText("INV-${invoice.invoiceId.takeLast(4).padStart(4, '0')}", endX, y, invNoPaint)
        y += 18f
        
        canvas.drawText(custName, startX, y, namePaint)
        canvas.drawText(dateStr, endX, y, datePaint)
        y += 14f
        
        if (invoice.customerPhone.isNotBlank()) {
            canvas.drawText(invoice.customerPhone, startX, y, Paint(addressPaint).apply { textAlign = Paint.Align.LEFT })
        }
        y += 24f

        // --- Table Header ---
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 14f
        
        canvas.drawText("ITEM", startX, y, tableHeaderPaint)
        canvas.drawText("QTY", colQtyX, y, Paint(tableHeaderPaint).apply { textAlign = Paint.Align.RIGHT })
        canvas.drawText("RATE", colRateX, y, Paint(tableHeaderPaint).apply { textAlign = Paint.Align.RIGHT })
        canvas.drawText("AMOUNT", endX, y, Paint(tableHeaderPaint).apply { textAlign = Paint.Align.RIGHT })
        
        y += 10f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 24f

        // --- Table Items ---
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
        }
        
        y += 6f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 24f

        // --- Summary ---
        val summaryLabelPaint = Paint(tableItemPaint).apply { 
            color = textGray 
            textAlign = Paint.Align.LEFT
        }
        val summaryValuePaint = Paint(tableItemPaint).apply { 
            typeface = sansSerifMedium 
            textAlign = Paint.Align.RIGHT
        }
        
        val summaryX = 220f
        val sym = invoice.currencySymbol
        
        canvas.drawText("Bill Amount", summaryX, y, summaryLabelPaint)
        canvas.drawText("$sym${formatCurrency(invoice.billAmount)}", endX, y, summaryValuePaint)
        y += 24f
        
        if (invoice.previousOutstanding > 0) {
            canvas.drawText("Prev. Outstanding", summaryX, y, summaryLabelPaint)
            canvas.drawText("+$sym${formatCurrency(invoice.previousOutstanding)}", endX, y, Paint(summaryValuePaint).apply { color = Color.rgb(220, 38, 38) })
            y += 24f
        }
        
        if (invoice.cashReceived > 0) {
            canvas.drawText("Cash Received", summaryX, y, summaryLabelPaint)
            canvas.drawText("-$sym${formatCurrency(invoice.cashReceived)}", endX, y, Paint(summaryValuePaint).apply { color = Color.rgb(22, 163, 74) })
            y += 24f
        }
        
        // --- Total Balance Box ---
        y += 8f
        val boxHeight = 44f
        val boxRect = android.graphics.RectF(summaryX - 12f, y, endX + 12f, y + boxHeight)
        
        val boxPaint = Paint().apply {
            color = primaryLight
            isAntiAlias = true
        }
        canvas.drawRoundRect(boxRect, 8f, 8f, boxPaint)
        
        val totalLabelPaint = Paint().apply {
            color = textDark
            textSize = 12f
            typeface = sansSerifMedium
            textAlign = Paint.Align.LEFT
            isAntiAlias = true
        }
        val totalValPaint = Paint(totalLabelPaint).apply { 
            color = primaryColor
            textSize = 18f
            typeface = sansSerifBold
            textAlign = Paint.Align.RIGHT
        }
        
        val totalY = y + (boxHeight / 2) + 6f
        canvas.drawText("Total Balance", summaryX, totalY, totalLabelPaint)
        canvas.drawText("$sym${formatCurrency(invoice.totalBalance)}", endX, totalY, totalValPaint)
        
        // Ensure there is enough space for the rest
        y += boxHeight + 30f
        canvas.drawLine(startX, y, endX, y, linePaint)
        
        // --- Footer (Positioned near the bottom) ---
        val thankYouPaint = Paint().apply {
            color = textGray
            textSize = 12f
            typeface = sansSerifMedium
            isAntiAlias = true
        }
        val sigNamePaint = Paint().apply {
            color = textDark
            textSize = 10f
            typeface = sansSerifBold
            textAlign = Paint.Align.RIGHT
            isAntiAlias = true
        }
        val sigTitlePaint = Paint(sigNamePaint).apply {
            textSize = 8f
            typeface = sansSerif
            color = textGray
        }
        
        // Bottom Text
        val bottomY = totalHeight - 20f
        val bottomPaint = Paint().apply {
            color = textLight
            textSize = 7f
            typeface = Typeface.create(Typeface.SANS_SERIF, Typeface.ITALIC)
            textAlign = Paint.Align.CENTER
            isAntiAlias = true
        }
        canvas.drawText("This is a computer-generated invoice, does not require a physical signature", centerX, bottomY, bottomPaint)

        // Footer elements just above the bottom note
        val footerY = bottomY - 30f
        
        canvas.drawText("Thank you for shopping with us!", startX, footerY - 10f, thankYouPaint)
        
        val ownerStr = if (invoice.ownerName.isNotBlank()) invoice.ownerName else "Store Owner"
        canvas.drawLine(endX - 90f, footerY - 20f, endX, footerY - 20f, linePaint)
        canvas.drawText(ownerStr, endX, footerY - 4f, sigNamePaint)
        canvas.drawText("Authorized Signatory", endX, footerY + 8f, sigTitlePaint)

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

