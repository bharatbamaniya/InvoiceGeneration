import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    text = f.read()

text = text.replace("fun addInventoryItem(name: String, price: Double, unit: String) {", "fun addInventoryItem(name: String, price: Double, unit: String, iconEmoji: String = \"\") {")
text = text.replace("unit = unit,\n        )", "unit = unit,\n            iconEmoji = iconEmoji\n        )")
text = text.replace("unit = unit\n        )", "unit = unit,\n            iconEmoji = iconEmoji\n        )")
text = text.replace("            unit = unit,", "            unit = unit,\n            iconEmoji = iconEmoji,")

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(text)

