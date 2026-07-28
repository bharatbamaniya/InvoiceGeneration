import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace("    init {\n        _uiState.update { it.copy(inventoryItems = defaultVeggieCatalog) }", "    init {\n        repository.syncFromFirebase()\n        _uiState.update { it.copy(inventoryItems = defaultVeggieCatalog) }")

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
