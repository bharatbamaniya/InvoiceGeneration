import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

# Fix addCustomItem
old_add_custom = """        _uiState.update { state ->
            state.copy(inventoryItems = state.inventoryItems + newItem)
        }
        addItemToCart(newItem)"""

new_add_custom = """        viewModelScope.launch {
            repository.insertItem(newItem)
        }
        addItemToCart(newItem)"""
content = content.replace(old_add_custom, new_add_custom)

# Fix addInventoryItem
old_add_inv = """        _uiState.update { state ->
            state.copy(inventoryItems = state.inventoryItems + newItem)
        }"""
new_add_inv = """        viewModelScope.launch {
            repository.insertItem(newItem)
        }"""
content = content.replace(old_add_inv, new_add_inv)

# Fix updateInventoryItem
old_update_inv = """        _uiState.update { state ->
            state.copy(inventoryItems = state.inventoryItems.map { if (it.id == updatedItem.id) updatedItem else it })
        }"""
new_update_inv = """        viewModelScope.launch {
            repository.updateItem(updatedItem)
        }"""
content = content.replace(old_update_inv, new_update_inv)

# Fix deleteInventoryItem
old_delete_inv = """        _uiState.update { state ->
            state.copy(inventoryItems = state.inventoryItems.filter { it.id != itemId })
        }"""
new_delete_inv = """        viewModelScope.launch {
            repository.deleteItem(itemId)
        }"""
content = content.replace(old_delete_inv, new_delete_inv)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
