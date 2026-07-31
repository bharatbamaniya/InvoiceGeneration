import re

with open('app/src/main/java/com/example/ui/screens/InvoiceDetailScreen.kt', 'r') as f:
    text = f.read()

# Replace generatePdfUri body
start_marker = "fun generatePdfUri(context: Context, invoice: Invoice): android.net.Uri? {"
end_marker = "    } catch (e: Exception) {\n        e.printStackTrace()\n        return null\n    }\n}"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_marker)
    new_impl = """fun generatePdfUri(context: Context, invoice: Invoice): android.net.Uri? {
    val file = com.example.util.PdfInvoiceGenerator.createPdfInvoice(context, invoice)
    return if (file != null) {
        com.example.util.PdfInvoiceGenerator.getPdfUri(context, file)
    } else {
        null
    }
}"""
    text = text[:start_idx] + new_impl + text[end_idx:]

with open('app/src/main/java/com/example/ui/screens/InvoiceDetailScreen.kt', 'w') as f:
    f.write(text)
