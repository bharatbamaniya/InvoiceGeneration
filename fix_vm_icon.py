with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    text = f.read()

text = text.replace("""    fun addCustomItem(name: String, price: Double, unit: String = "kg") {
        if (name.isBlank() || price <= 0.0) return
        val newItem = GroceryItem(
            id = "custom_${System.currentTimeMillis()}",
            name = name.trim(),
            price = price,
            unit = unit,
            iconEmoji = iconEmoji,
        )""", """    fun addCustomItem(name: String, price: Double, unit: String = "kg") {
        if (name.isBlank() || price <= 0.0) return
        val newItem = GroceryItem(
            id = "custom_${System.currentTimeMillis()}",
            name = name.trim(),
            price = price,
            unit = unit,
            iconEmoji = "📦"
        )""")

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(text)
