import re

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'r') as f:
    content = f.read()

new_create_method = """    fun createPdfInvoice(context: Context, invoice: Invoice): File? {
        val pdfDocument = PdfDocument()
        
        val baseHeight = 700f
        val itemHeight = 30f
        val totalHeight = (baseHeight + (invoice.items.size * itemHeight)).toInt()
        val pageWidth = 400
        val pageInfo = PdfDocument.PageInfo.Builder(pageWidth, totalHeight, 1).create()
        val page = pdfDocument.startPage(pageInfo)
        val canvas = page.canvas

        canvas.drawColor(Color.WHITE)

        val blackPaint = Paint().apply {
            color = Color.BLACK
            isAntiAlias = true
            typeface = Typeface.MONOSPACE
        }
        val grayPaint = Paint(blackPaint).apply { color = Color.DKGRAY }
        val lightGrayPaint = Paint(blackPaint).apply { color = Color.GRAY }
        val boldPaint = Paint(blackPaint).apply { 
            typeface = Typeface.create(Typeface.MONOSPACE, Typeface.BOLD) 
        }
        
        val centerPaint = Paint(blackPaint).apply { textAlign = Paint.Align.CENTER }
        val centerBoldPaint = Paint(boldPaint).apply { textAlign = Paint.Align.CENTER; color = Color.rgb(27, 94, 32) } // #1B5E20
        
        val rightPaint = Paint(blackPaint).apply { textAlign = Paint.Align.RIGHT }
        val rightBoldPaint = Paint(boldPaint).apply { textAlign = Paint.Align.RIGHT }
        val rightGreenBoldPaint = Paint(boldPaint).apply { textAlign = Paint.Align.RIGHT; color = Color.rgb(27, 94, 32) }
        
        val startX = 20f
        val colQtyX = 180f
        val colRateX = 280f
        val endX = pageWidth - 20f
        val centerX = pageWidth / 2f
        var y = 40f
        
        // Header
        centerBoldPaint.textSize = 24f
        canvas.drawText("🛒 ${invoice.storeName}", centerX, y, centerBoldPaint)
        y += 20f

        centerPaint.textSize = 12f
        centerPaint.color = Color.DKGRAY
        if (invoice.storeAddress.isNotBlank()) {
            canvas.drawText(invoice.storeAddress, centerX, y, centerPaint)
            y += 16f
        }
        if (invoice.storePhone.isNotBlank()) {
            canvas.drawText("Phone: ${invoice.storePhone}", centerX, y, centerPaint)
            y += 20f
        }
        
        y += 10f
        val linePaint = Paint().apply { color = Color.LTGRAY; strokeWidth = 1f }
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 20f
        
        // Customer & Invoice Metadata
        lightGrayPaint.textSize = 10f
        boldPaint.textSize = 10f
        rightPaint.textSize = 10f
        
        canvas.drawText("CUSTOMER:", startX, y, boldPaint)
        canvas.drawText("INVOICE NO:", endX, y, Paint(rightPaint).apply { color = Color.GRAY; typeface = Typeface.create(Typeface.MONOSPACE, Typeface.BOLD) })
        y += 16f
        
        blackPaint.textSize = 14f
        boldPaint.textSize = 14f
        rightGreenBoldPaint.textSize = 14f
        
        val custName = if (invoice.customerName.isNotBlank()) invoice.customerName else "Walk-in Customer"
        canvas.drawText(custName, startX, y, boldPaint)
        canvas.drawText("#${invoice.invoiceId}", endX, y, rightGreenBoldPaint)
        
        y += 16f
        val sdf = SimpleDateFormat("dd MMM yyyy, hh:mm a", Locale.US)
        val rightGrayPaint = Paint(rightPaint).apply { color = Color.DKGRAY; textSize = 11f }
        canvas.drawText(sdf.format(Date(invoice.dateMillis)), endX, y, rightGrayPaint)
        
        y += 20f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 24f
        
        // Table Header
        val headerPaint = Paint(boldPaint).apply { color = Color.GRAY; textSize = 11f }
        canvas.drawText("ITEM", startX, y, headerPaint)
        canvas.drawText("QTY", colQtyX, y, Paint(headerPaint).apply{textAlign=Paint.Align.CENTER})
        canvas.drawText("RATE", colRateX, y, Paint(headerPaint).apply{textAlign=Paint.Align.CENTER})
        canvas.drawText("PRICE", endX, y, Paint(headerPaint).apply{textAlign=Paint.Align.RIGHT})
        
        y += 16f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 24f
        
        // Items
        blackPaint.textSize = 13f
        rightBoldPaint.textSize = 13f
        
        invoice.items.forEach { item ->
            val itemName = if (item.item.name.length > 15) item.item.name.substring(0, 13) + ".." else item.item.name
            canvas.drawText(itemName, startX, y, Paint(blackPaint).apply{ typeface = Typeface.create(Typeface.MONOSPACE, Typeface.BOLD)})
            
            val qtyVal = item.quantity
            val qtyStr = if (qtyVal % 1.0 == 0.0) qtyVal.toInt().toString() else qtyVal.toString()
            canvas.drawText(qtyStr, colQtyX, y, Paint(blackPaint).apply{textAlign=Paint.Align.CENTER; typeface = Typeface.create(Typeface.MONOSPACE, Typeface.BOLD)})
            
            val rateStr = String.format(Locale.US, "%.2f/%s", item.unitPrice, item.item.unit)
            canvas.drawText(rateStr, colRateX, y, Paint(blackPaint).apply{textAlign=Paint.Align.CENTER; color=Color.DKGRAY; textSize=11f})
            
            val totalStr = String.format(Locale.US, "%s%.2f", invoice.currencySymbol, item.totalPrice)
            canvas.drawText(totalStr, endX, y, rightBoldPaint)
            y += 24f
        }
        
        y += 10f
        canvas.drawLine(startX, y, endX, y, linePaint)
        y += 30f
        
        // Totals
        val normalText = Paint(blackPaint).apply { color = Color.DKGRAY; textSize = 13f }
        val rightNormalText = Paint(rightPaint).apply { color = Color.DKGRAY; textSize = 13f }
        
        canvas.drawText("Bill Amount", startX, y, normalText)
        canvas.drawText(String.format(Locale.US, "%s%.2f", invoice.currencySymbol, invoice.billAmount), endX, y, rightNormalText)
        
        y += 24f
        
        if (invoice.previousOutstanding > 0) {
            canvas.drawText("Previous Outstanding", startX, y, normalText)
            canvas.drawText(String.format(Locale.US, "+%s%.2f", invoice.currencySymbol, invoice.previousOutstanding), endX, y, rightNormalText)
            y += 24f
        }
        
        if (invoice.cashReceived > 0) {
            canvas.drawText("Cash Received", startX, y, Paint(normalText).apply{color=Color.rgb(198,40,40)})
            canvas.drawText(String.format(Locale.US, "-%s%.2f", invoice.currencySymbol, invoice.cashReceived), endX, y, Paint(rightNormalText).apply{color=Color.rgb(198,40,40)})
            y += 24f
        }
        
        y += 10f
        // Box for Total Balance
        val rectPaint = Paint().apply { color = Color.rgb(232, 245, 233); style = Paint.Style.FILL }
        canvas.drawRoundRect(startX, y-20f, endX, y+20f, 8f, 8f, rectPaint)
        
        val totalLabelPaint = Paint(boldPaint).apply { color = Color.rgb(27, 94, 32); textSize = 14f }
        val totalValuePaint = Paint(rightBoldPaint).apply { color = Color.rgb(27, 94, 32); textSize = 18f }
        canvas.drawText("TOTAL BALANCE", startX + 10f, y + 6f, totalLabelPaint)
        canvas.drawText(String.format(Locale.US, "%s%.2f", invoice.currencySymbol, invoice.totalBalance), endX - 10f, y + 6f, totalValuePaint)
        
        y += 40f
        
        val footerPaint = Paint(centerPaint).apply { color = Color.GRAY; textSize = 11f }
        canvas.drawText("Thank you for shopping at ${invoice.storeName}! 🙏", centerX, y, footerPaint)
        
        y += 50f
        // Signature
        val sigTitle = Paint(rightPaint).apply { color = Color.DKGRAY; textSize = 11f }
        canvas.drawText("Authorized Signatory", endX, y, sigTitle)
        y += 20f
        val ownerSignature = if (invoice.ownerName.isNotBlank()) invoice.ownerName else "Owner Name"
        canvas.drawText(ownerSignature, endX, y, Paint(rightBoldPaint).apply { textSize = 13f })
        
        pdfDocument.finishPage(page)
        
        val pdfFile = File(context.cacheDir, "Invoice_${invoice.invoiceId}.pdf")
        return try {
            val fos = FileOutputStream(pdfFile)
            pdfDocument.writeTo(fos)
            fos.close()
            pdfDocument.close()
            pdfFile
        } catch (e: Exception) {
            e.printStackTrace()
            pdfDocument.close()
            null
        }
    }"""

# regex replace
content = re.sub(r'    fun createPdfInvoice\(context: Context, invoice: Invoice\): File\? \{.*?(?=    /\*\*|    fun getPdfUri)', new_create_method + "\n\n", content, flags=re.DOTALL)

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'w') as f:
    f.write(content)

