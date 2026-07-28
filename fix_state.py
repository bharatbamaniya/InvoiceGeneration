import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val editingInvoiceId: String? = null',
    'val editingInvoiceId: String? = null,\n    val swipeToDeleteEnabled: Boolean = true'
)

content = content.replace(
    'fun updateStoreSettings(name: String, address: String, phone: String, owner: String, currency: String) {',
    'fun updateStoreSettings(name: String, address: String, phone: String, owner: String, currency: String, swipeToDelete: Boolean = true) {'
)

content = content.replace(
    '                currencySymbol = currency.ifBlank { "₹" }',
    '                currencySymbol = currency.ifBlank { "₹" },\n                swipeToDeleteEnabled = swipeToDelete'
)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
