import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

new_logout = """    fun logout() {
        viewModelScope.launch {
            repository.clearLocalData()
            repository.setStoreUid("")
            _uiState.update { 
                it.copy(
                    isAuthenticated = false, 
                    storeUid = "",
                    customers = emptyList(),
                    invoiceHistory = emptyList(),
                    inventoryItems = defaultVeggieCatalog,
                    payments = emptyList()
                ) 
            }
        }
    }"""
    
content = content.replace("""    fun logout() {
        repository.setStoreUid("") // or clear it
        _uiState.update { it.copy(isAuthenticated = false, storeUid = "") }
    }""", new_logout)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
