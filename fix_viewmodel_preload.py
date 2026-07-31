import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    text = f.read()

# Add more items to defaultVeggieCatalog
old_catalog = """    val defaultVeggieCatalog = listOf(
        GroceryItem("v1", "Potato", 30.0, "kg", "🥔"),
        GroceryItem("v2", "Onion", 40.0, "kg", "🧅"),
        GroceryItem("v3", "Tomato", 50.0, "kg", "🍅"),
        GroceryItem("v4", "Cabbage", 30.0, "pc", "🥬"),
        GroceryItem("v5", "Cauliflower", 40.0, "pc", "🥦"),
        GroceryItem("v6", "Carrot", 60.0, "kg", "🥕"),
        GroceryItem("v7", "Spinach", 20.0, "bunch", "🥬"),
        GroceryItem("v8", "Green Peas", 80.0, "kg", "🫛"),
        GroceryItem("v9", "Cucumber", 30.0, "kg", "🥒"),
        GroceryItem("v10", "Capsicum", 60.0, "kg", "🫑"),
        GroceryItem("v11", "Eggplant", 40.0, "kg", "🍆"),
        GroceryItem("v12", "Garlic", 120.0, "kg", "🧄")
    )"""

new_catalog = """    val defaultVeggieCatalog = listOf(
        GroceryItem("v1", "Potato", 30.0, "kg", "🥔"),
        GroceryItem("v2", "Onion", 40.0, "kg", "🧅"),
        GroceryItem("v3", "Tomato", 50.0, "kg", "🍅"),
        GroceryItem("v4", "Cabbage", 30.0, "pc", "🥬"),
        GroceryItem("v5", "Cauliflower", 40.0, "pc", "🥦"),
        GroceryItem("v6", "Carrot", 60.0, "kg", "🥕"),
        GroceryItem("v7", "Spinach", 20.0, "bunch", "🥬"),
        GroceryItem("v8", "Green Peas", 80.0, "kg", "🫛"),
        GroceryItem("v9", "Cucumber", 30.0, "kg", "🥒"),
        GroceryItem("v10", "Capsicum", 60.0, "kg", "🫑"),
        GroceryItem("v11", "Eggplant", 40.0, "kg", "🍆"),
        GroceryItem("v12", "Garlic", 120.0, "kg", "🧄"),
        GroceryItem("v13", "Ginger", 150.0, "kg", "🫚"),
        GroceryItem("v14", "Green Chili", 100.0, "kg", "🌶️"),
        GroceryItem("v15", "Coriander", 15.0, "bunch", "🌿"),
        GroceryItem("v16", "Mint", 10.0, "bunch", "🌿"),
        GroceryItem("v17", "Radish", 20.0, "kg", "🥕"),
        GroceryItem("v18", "Bitter Gourd", 50.0, "kg", "🥒"),
        GroceryItem("v19", "Bottle Gourd", 25.0, "pc", "🥒"),
        GroceryItem("v20", "Pumpkin", 40.0, "kg", "🎃")
    )"""

text = text.replace(old_catalog, new_catalog)

# Modify the init block to preload
old_init = """        viewModelScope.launch {
            repository.allItems.collect { items ->
                _uiState.update { it.copy(inventoryItems = if (items.isEmpty()) defaultVeggieCatalog else items) }
            }
        }"""

new_init = """        viewModelScope.launch {
            repository.allItems.collect { items ->
                if (items.isEmpty()) {
                    defaultVeggieCatalog.forEach { repository.insertItem(it) }
                    _uiState.update { it.copy(inventoryItems = defaultVeggieCatalog) }
                } else {
                    _uiState.update { it.copy(inventoryItems = items) }
                }
            }
        }"""

text = text.replace(old_init, new_init)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(text)

