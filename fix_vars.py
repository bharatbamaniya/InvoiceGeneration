import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    content = f.read()

vars_decl = """    val filteredItems = if (state.searchQuery.isEmpty()) {
        allAvailableItems
    } else {
        allAvailableItems.filter { it.name.contains(state.searchQuery, ignoreCase = true) }
    }
    
    val subtotalAmount = state.cartItems.sumOf { it.customPrice * it.quantity }
    val totalCartCount = state.cartItems.sumOf { it.quantity }
    val totalCartCountStr = if (totalCartCount % 1.0 == 0.0) totalCartCount.toInt().toString() else String.format(Locale.US, "%.2f", totalCartCount)
    
    val totalBalance = subtotalAmount
"""

content = content.replace("    val allAvailableItems = state.inventoryItems", "    val allAvailableItems = state.inventoryItems\n" + vars_decl)
content = content.replace("    val totalBalance = state.cartItems.sumOf { it.customPrice * it.quantity }", "")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(content)

