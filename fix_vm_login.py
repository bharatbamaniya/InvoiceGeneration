import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

old_login = """    fun login(storeUid: String) {
        if (storeUid.isNotBlank()) {
            repository.setStoreUid(storeUid)
            _uiState.update { it.copy(isAuthenticated = true, storeUid = storeUid) }
        }
    }
    
    fun registerNewStore() {
        val newUid = UUID.randomUUID().toString().take(8).uppercase()
        repository.setStoreUid(newUid)
        _uiState.update { it.copy(isAuthenticated = true, storeUid = newUid) }
    }"""
    
new_login = """    fun login(storeUid: String) {
        if (storeUid.isNotBlank()) {
            viewModelScope.launch {
                repository.clearLocalData()
                repository.setStoreUid(storeUid)
                _uiState.update { it.copy(isAuthenticated = true, storeUid = storeUid) }
            }
        }
    }
    
    fun registerNewStore() {
        viewModelScope.launch {
            repository.clearLocalData()
            val newUid = UUID.randomUUID().toString().take(8).uppercase()
            repository.setStoreUid(newUid)
            _uiState.update { it.copy(isAuthenticated = true, storeUid = newUid) }
        }
    }"""

content = content.replace(old_login, new_login)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
