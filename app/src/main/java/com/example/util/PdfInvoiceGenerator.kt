package com.example.util

import android.content.Context
import android.content.Intent
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
import android.net.Uri
import android.print.PrintAttributes
import android.print.PrintDocumentAdapter
import android.print.PrintManager
import android.widget.Toast
import androidx.core.content.FileProvider
import com.example.model.Invoice
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.net.URLEncoder
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object PdfInvoiceGenerator {

    /**
     * Generates a PDF File for the given Invoice and returns the Uri via FileProvider.
     */
    fun createPdfInvoice(context: Context, invoice: Invoice): File? {
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
        val sansSerif = Typeface.create(Typeface.SANS_SERIF, Typeface.NORMAL)
        val sansSerifBold = Typeface.create(Typeface.SANS_SERIF, Typeface.BOLD)

        val titlePaint = Paint().apply {
            color = primaryColor
            textSize = 28f
            typeface = sansSerifBold
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
            typeface = sansSerifBold
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
            textSize = 14f // Reduced size
            typeface = sansSerifBold
            textAlign = Paint.Align.RIGHT
            isAntiAlias = true
        }

        val datePaint = Paint().apply {
            color = textDark
            textSize = 10f
            typeface = sansSerif
            textAlign = Paint.Align.RIGHT
            isAntiAlias = true
        }

        val tableHeaderPaint = Paint().apply {
            color = textGray
            textSize = 9f
            typeface = sansSerifBold
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

        val margin = 30f
        val startX = margin
        val endX = pageWidth - margin
        val centerX = pageWidth / 2f
        
        val colQtyX = 220f
        val colRateX = 300f
        
        var y = 50f

        // --- Header ---
        canvas.drawText(invoice.storeName, centerX, y, titlePaint)
        y += 18f
        
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
        val sym = invoice.currencySymbol
        invoice.items.forEach { item ->
            canvas.drawText(item.item.name, startX, y, tableItemPaint)
            
            val qtyStr = if (item.quantity % 1.0 == 0.0) "${item.quantity.toInt()}" else "${item.quantity}"
            val rateStr = "$sym${formatCurrency(item.unitPrice)}/${item.item.unit}"
            
            canvas.drawText(qtyStr, colQtyX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            canvas.drawText(rateStr, colRateX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            canvas.drawText("$sym${formatCurrency(item.totalPrice)}", endX, y, Paint(tableItemPaint).apply { textAlign = Paint.Align.RIGHT })
            
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
            typeface = sansSerifBold
            textAlign = Paint.Align.RIGHT
        }
        
        val summaryX = 180f
        
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
        val boxRect = android.graphics.RectF(summaryX - 8f, y, endX + 8f, y + boxHeight)
        
        val boxPaint = Paint().apply {
            color = primaryLight
            isAntiAlias = true
        }
        canvas.drawRoundRect(boxRect, 8f, 8f, boxPaint)
        
        val totalLabelPaint = Paint().apply {
            color = textDark
            textSize = 12f
            typeface = sansSerifBold
            textAlign = Paint.Align.LEFT
            isAntiAlias = true
        }
        val totalValPaint = Paint(totalLabelPaint).apply { 
            color = primaryColor
            textSize = 18f
            typeface = sansSerifBold
            textAlign = Paint.Align.RIGHT
        }
        
        val totalY = y + (boxHeight / 2) + 5f
        canvas.drawText("Total Balance", summaryX, totalY, totalLabelPaint)
        canvas.drawText("$sym${formatCurrency(invoice.totalBalance)}", endX, totalY, totalValPaint)
        
        // --- Footer ---
        val thankYouPaint = Paint().apply {
            color = textGray
            textSize = 12f
            typeface = sansSerifBold
            textAlign = Paint.Align.LEFT
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
        
        val bottomY = totalHeight - 20f
        val bottomPaint = Paint().apply {
            color = textLight
            textSize = 7f
            typeface = Typeface.create(Typeface.SANS_SERIF, Typeface.ITALIC)
            textAlign = Paint.Align.CENTER
            isAntiAlias = true
        }
        canvas.drawText("This is a computer-generated invoice, does not require a physical signature", centerX, bottomY, bottomPaint)

        val footerY = bottomY - 35f
        
        if (y + boxHeight + 40f < footerY - 20f) {
            canvas.drawLine(startX, footerY - 30f, endX, footerY - 30f, linePaint)
        }
        
        canvas.drawText("Thank you for shopping with us!", startX, footerY - 5f, thankYouPaint)
        
        val ownerStr = if (invoice.ownerName.isNotBlank()) invoice.ownerName else "Store Owner"
        canvas.drawLine(endX - 90f, footerY - 15f, endX, footerY - 15f, linePaint)
        canvas.drawText(ownerStr, endX, footerY - 1f, sigNamePaint)
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
    fun getPdfUri(context: Context, pdfFile: File): Uri {
        return FileProvider.getUriForFile(
            context,
            "${context.packageName}.fileprovider",
            pdfFile
        )
    }

    /**
     * Shares the PDF directly to WhatsApp.
     */
    fun sharePdfToWhatsApp(context: Context, pdfFile: File, customerPhone: String = "") {
        val uri = getPdfUri(context, pdfFile)

        val shareIntent = Intent(Intent.ACTION_SEND).apply {
            type = "application/pdf"
            putExtra(Intent.EXTRA_STREAM, uri)
            putExtra(Intent.EXTRA_SUBJECT, "Invoice ${pdfFile.name}")
            putExtra(Intent.EXTRA_TEXT, "Please find attached your invoice.")
            clipData = android.content.ClipData.newRawUri("", uri)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }

        try {
            shareIntent.setPackage("com.whatsapp")
            context.startActivity(shareIntent)
        } catch (e: Exception) {
            try {
                shareIntent.setPackage("com.whatsapp.w4b")
                context.startActivity(shareIntent)
            } catch (e2: Exception) {
                // WhatsApp not installed, fallback to normal share
                val chooserIntent = Intent.createChooser(shareIntent.apply { setPackage(null) }, "Share Invoice PDF via")
                context.startActivity(chooserIntent)
            }
        }
    }

    /**
     * Formats WhatsApp Text Message with itemized breakdown
     */
    fun formatWhatsAppText(invoice: Invoice): String {
        val dateFormat = SimpleDateFormat("dd MMM yyyy, hh:mm a", Locale.getDefault())
        val dateStr = dateFormat.format(Date(invoice.dateMillis))

        val custName = if (invoice.customerName.isBlank()) "Valued Customer" else invoice.customerName

        val sb = StringBuilder()
        sb.append("🧾 *INVOICE FROM ${invoice.storeName.uppercase()}*\n")
        sb.append("----------------------------------\n")
        sb.append("📅 *Date:* $dateStr\n")
        sb.append("🆔 *Invoice #:* `${invoice.invoiceId}`\n")
        sb.append("👤 *Customer:* $custName\n\n")
        sb.append("🛒 *ITEMS PURCHASED:*\n")

        invoice.items.forEachIndexed { index, item ->
            val rate = String.format(Locale.US, "%.2f", item.unitPrice)
            val lineTotal = String.format(Locale.US, "%.2f", item.totalPrice)
            sb.append("${index + 1}. *${item.item.name}*\n")
            sb.append("    ${item.quantity} x ${invoice.currencySymbol}$rate = *${invoice.currencySymbol}$lineTotal*\n")
        }

        sb.append("----------------------------------\n")
        sb.append("💰 *Bill Amount:* ${invoice.currencySymbol}${String.format(Locale.US, "%.2f", invoice.billAmount)}\n")
        if (invoice.previousOutstanding > 0) {
            sb.append("📈 *Previous Outstanding:* +${invoice.currencySymbol}${String.format(Locale.US, "%.2f", invoice.previousOutstanding)}\n")
        }
        if (invoice.cashReceived > 0) {
            sb.append("💵 *Cash Received:* -${invoice.currencySymbol}${String.format(Locale.US, "%.2f", invoice.cashReceived)}\n")
        }
        sb.append("💳 *TOTAL BALANCE:* *${invoice.currencySymbol}${String.format(Locale.US, "%.2f", invoice.totalBalance)}*\n")
        sb.append("----------------------------------\n")
        sb.append("Thank you for shopping with us! Have a great day! 🙏")

        return sb.toString()
    }

    /**
     * Opens WhatsApp with pre-filled message via https://wa.me/
     */
    fun sendWhatsAppMessage(context: Context, phone: String, message: String) {
        // Clean phone number (strip spaces, dashes, plus sign if formatting for wa.me)
        val cleanPhone = phone.replace(Regex("[^0-9]"), "")
        val encodedMsg = URLEncoder.encode(message, "UTF-8")

        val url = if (cleanPhone.isNotBlank()) {
            "https://wa.me/$cleanPhone?text=$encodedMsg"
        } else {
            "https://wa.me/?text=$encodedMsg"
        }

        val intent = Intent(Intent.ACTION_VIEW).apply {
            data = Uri.parse(url)
        }

        try {
            context.startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(context, "Could not open WhatsApp. Please check if installed.", Toast.LENGTH_LONG).show()
        }
    }

    /**
     * Shares the actual PDF document file via Android Intent (WhatsApp, Email, etc.)
     */
    fun sharePdfFile(context: Context, pdfFile: File, customerPhone: String = "") {
        val uri = getPdfUri(context, pdfFile)

        val shareIntent = Intent(Intent.ACTION_SEND).apply {
            type = "application/pdf"
            putExtra(Intent.EXTRA_STREAM, uri)
            putExtra(Intent.EXTRA_SUBJECT, "Invoice ${pdfFile.name}")
            clipData = android.content.ClipData.newRawUri("", uri)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }

        val chooserIntent = Intent.createChooser(shareIntent, "Share Invoice PDF via")
        try {
            context.startActivity(chooserIntent)
        } catch (e: Exception) {
            Toast.makeText(context, "Unable to share file: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

    /**
     * Shares the invoice as a formatted text message via Android Intent chooser
     */
    fun shareInvoiceText(context: Context, invoice: Invoice) {
        val text = formatWhatsAppText(invoice)
        val shareIntent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_SUBJECT, "Invoice ${invoice.invoiceId}")
            putExtra(Intent.EXTRA_TEXT, text)
        }
        val chooserIntent = Intent.createChooser(shareIntent, "Share Invoice via")
        try {
            context.startActivity(chooserIntent)
        } catch (e: Exception) {
            Toast.makeText(context, "Unable to share: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

    /**
     * Opens Android System Print Dialog for the generated PDF
     */
    fun printPdfInvoice(context: Context, pdfFile: File) {
        val printManager = context.getSystemService(Context.PRINT_SERVICE) as? PrintManager
        if (printManager == null) {
            Toast.makeText(context, "Printing not supported on this device.", Toast.LENGTH_SHORT).show()
            return
        }

        val printAdapter = object : PrintDocumentAdapter() {
            override fun onLayout(
                oldAttributes: PrintAttributes?,
                newAttributes: PrintAttributes?,
                cancellationSignal: android.os.CancellationSignal?,
                callback: LayoutResultCallback?,
                extras: android.os.Bundle?
            ) {
                if (cancellationSignal?.isCanceled == true) {
                    callback?.onLayoutCancelled()
                    return
                }
                val info = android.print.PrintDocumentInfo.Builder(pdfFile.name)
                    .setContentType(android.print.PrintDocumentInfo.CONTENT_TYPE_DOCUMENT)
                    .setPageCount(1)
                    .build()
                callback?.onLayoutFinished(info, true)
            }

            override fun onWrite(
                pages: Array<out android.print.PageRange>?,
                destination: android.os.ParcelFileDescriptor?,
                cancellationSignal: android.os.CancellationSignal?,
                callback: WriteResultCallback?
            ) {
                try {
                    val input = pdfFile.inputStream()
                    val output = FileOutputStream(destination?.fileDescriptor)
                    input.copyTo(output)
                    input.close()
                    output.close()
                    callback?.onWriteFinished(arrayOf(android.print.PageRange.ALL_PAGES))
                } catch (e: Exception) {
                    callback?.onWriteFailed(e.message)
                }
            }
        }

        try {
            printManager.print("Invoice_${pdfFile.name}", printAdapter, null)
        } catch (e: Exception) {
            Toast.makeText(context, "Error printing document: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }
}
