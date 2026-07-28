import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

old_inv_gen = 'val invNumber = state.editingInvoiceId ?: ("INV-" + (1000..9999).random())'
new_inv_gen = """val invNumber = state.editingInvoiceId ?: run {
            val maxId = state.invoiceHistory.maxOfOrNull { 
                it.invoiceId.removePrefix("INV-").toIntOrNull() ?: 0 
            } ?: 0
            "INV-" + (maxId + 1).toString().padStart(4, '0')
        }"""

content = content.replace(old_inv_gen, new_inv_gen)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
