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
    }

    /**
     * Get a Content Uri for sharing via FileProvider
     */
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
