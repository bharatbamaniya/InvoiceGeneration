with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'import com.example.model.InvoiceItem',
    'import com.example.model.InvoiceItem\nimport com.example.model.Customer\nimport com.example.model.Payment'
)

content = content.replace(
    'val invoiceHistory: List<Invoice> = emptyList(),',
    'val invoiceHistory: List<Invoice> = emptyList(),\n    val customers: List<Customer> = emptyList(),\n    val selectedCustomerId: String? = null,\n    val payments: List<Payment> = emptyList(),'
)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
