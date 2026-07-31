import re

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'r') as f:
    text = f.read()

# Make thankYouPaint center-aligned
text = text.replace("""        val thankYouPaint = Paint().apply {
            color = textGray
            textSize = 12f
            typeface = sansSerifBold
            isAntiAlias = true
        }""", """        val thankYouPaint = Paint().apply {
            color = textGray
            textSize = 12f
            typeface = sansSerifBold
            textAlign = Paint.Align.CENTER
            isAntiAlias = true
        }""")

# Update the drawText call for Thank you to use centerX
text = text.replace("""        canvas.drawText("Thank you for shopping with us!", startX, footerY - 5f, thankYouPaint)""", """        canvas.drawText("Thank you for shopping with us!", centerX, footerY - 5f, thankYouPaint)""")

with open('app/src/main/java/com/example/util/PdfInvoiceGenerator.kt', 'w') as f:
    f.write(text)

