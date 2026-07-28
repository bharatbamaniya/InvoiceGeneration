import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

# Update init block to load local settings first
init_pattern = r'init\s*\{'
new_init = """init {
        val localSettings = repository.getLocalStoreSettings()
        _uiState.update { 
            it.copy(
                storeName = localSettings["storeName"] as String,
                storeAddress = localSettings["storeAddress"] as String,
                storePhone = localSettings["storePhone"] as String,
                ownerName = localSettings["ownerName"] as String,
                currencySymbol = localSettings["currencySymbol"] as String,
                swipeToDeleteEnabled = localSettings["swipeToDelete"] as Boolean
            )
        }
"""
content = re.sub(init_pattern, new_init, content, count=1)

# Update updateStoreSettings
old_update_settings = """    fun updateStoreSettings(name: String, address: String, phone: String, owner: String, currency: String, swipeToDelete: Boolean = true) {
        _uiState.update {
            it.copy(
                storeName = name.ifBlank { "Fresh Veggies Market" },
                storeAddress = address,
                storePhone = phone,
                ownerName = owner.ifBlank { "Owner Name" },
                currencySymbol = currency.ifBlank { "₹" },
                swipeToDeleteEnabled = swipeToDelete
            )
        }
    }"""
    
new_update_settings = """    fun updateStoreSettings(name: String, address: String, phone: String, owner: String, currency: String, swipeToDelete: Boolean = true) {
        val safeName = name.ifBlank { "Fresh Veggies Market" }
        val safeOwner = owner.ifBlank { "Owner Name" }
        val safeCurrency = currency.ifBlank { "₹" }
        
        repository.saveStoreSettings(safeName, address, phone, safeOwner, safeCurrency, swipeToDelete)
        
        _uiState.update {
            it.copy(
                storeName = safeName,
                storeAddress = address,
                storePhone = phone,
                ownerName = safeOwner,
                currencySymbol = safeCurrency,
                swipeToDeleteEnabled = swipeToDelete
            )
        }
    }"""
content = content.replace(old_update_settings, new_update_settings)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)

