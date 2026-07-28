import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

# Update InvoiceUiState to remove currencySymbol? Wait, if we keep val currencySymbol: String = "₹", we don't need to change other places that read it, just places that write it.
content = content.replace('val currencySymbol: String = "₹",', 'val currencySymbol: String = "₹",')

# Update updateStoreSettings in InvoiceViewModel
old_update_settings = """    fun updateStoreSettings(name: String, address: String, phone: String, owner: String, currency: String, swipeToDelete: Boolean = true) {
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
    
new_update_settings = """    fun updateStoreSettings(name: String, address: String, phone: String, owner: String, swipeToDelete: Boolean = true) {
        val safeName = name.ifBlank { "Fresh Veggies Market" }
        val safeOwner = owner.ifBlank { "Owner Name" }
        
        repository.saveStoreSettings(safeName, address, phone, safeOwner, "₹", swipeToDelete)
        
        _uiState.update {
            it.copy(
                storeName = safeName,
                storeAddress = address,
                storePhone = phone,
                ownerName = safeOwner,
                swipeToDeleteEnabled = swipeToDelete
            )
        }
    }"""
    
content = content.replace(old_update_settings, new_update_settings)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)

