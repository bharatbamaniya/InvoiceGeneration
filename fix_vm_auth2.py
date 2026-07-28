import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

old_register = """    fun registerNewStore() {
        viewModelScope.launch {
            repository.clearLocalData()
            val newUid = UUID.randomUUID().toString().take(8).uppercase()
            repository.setStoreUid(newUid)
            _uiState.update { it.copy(isAuthenticated = true, storeUid = newUid) }
        }
    }"""
    
content = content.replace(old_register, "")

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)

