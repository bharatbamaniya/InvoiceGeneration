import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

# Add isAuthenticated and storeUid to InvoiceUiState
ui_state_pattern = r'val swipeToDeleteEnabled: Boolean = true\n\)'
new_ui_state = 'val swipeToDeleteEnabled: Boolean = true,\n    val isAuthenticated: Boolean = false,\n    val storeUid: String = ""\n)'
content = re.sub(ui_state_pattern, new_ui_state, content)

# In init, set isAuthenticated
init_pattern = r'val localSettings = repository\.getLocalStoreSettings\(\)'
new_init = """val localSettings = repository.getLocalStoreSettings()
        val uid = repository.getStoreUid()
        _uiState.update { it.copy(isAuthenticated = uid != null, storeUid = uid ?: "") }"""
content = content.replace('val localSettings = repository.getLocalStoreSettings()', new_init)

# Add login / register functions
auth_funcs = """
    fun login(storeUid: String) {
        if (storeUid.isNotBlank()) {
            repository.setStoreUid(storeUid)
            _uiState.update { it.copy(isAuthenticated = true, storeUid = storeUid) }
        }
    }
    
    fun registerNewStore() {
        val newUid = UUID.randomUUID().toString().take(8).uppercase()
        repository.setStoreUid(newUid)
        _uiState.update { it.copy(isAuthenticated = true, storeUid = newUid) }
    }
    
    fun logout() {
        repository.setStoreUid("") // or clear it
        _uiState.update { it.copy(isAuthenticated = false, storeUid = "") }
    }
"""

content = content.replace("    fun updateCustomerName(", auth_funcs + "\n    fun updateCustomerName(")

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)

