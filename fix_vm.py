import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

# Remove selectedCategory
content = re.sub(r'\s*val selectedCategory: String = "All",\n', '\n', content)

# Remove updateCategory
content = re.sub(r'    fun updateCategory\(category: String\) \{\n        _uiState.update \{ it.copy\(selectedCategory = category\) \}\n    \}\n\n', '', content)

# update addCustomItem
content = re.sub(r'fun addCustomItem\(name: String, price: Double, category: String = "Other", unit: String = "kg"\)', 'fun addCustomItem(name: String, price: Double, unit: String = "kg")', content)
content = re.sub(r'            category = category,\n', '', content)

# update addInventoryItem
content = re.sub(r'fun addInventoryItem\(name: String, price: Double, category: String, unit: String\)', 'fun addInventoryItem(name: String, price: Double, unit: String)', content)
content = re.sub(r'            category = category,\n', '', content)

# update GroceryItem creations in default catalog
# GroceryItem("v1", "Potato", 30.0, "Root", "kg", "🥔"),
content = re.sub(r'GroceryItem\(([^,]+),\s*([^,]+),\s*([^,]+),\s*"[^"]+",\s*([^,]+),\s*([^)]+)\)', r'GroceryItem(\1, \2, \3, \4, \5)', content)

# Some might not have all arguments explicit if default used, but they were defined as: GroceryItem("v1", "Potato", 30.0, "Root", "kg", "🥔")

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
