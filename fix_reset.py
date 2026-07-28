with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'customerPhone = "",\n                previousOutstanding = 0.0,',
    'customerPhone = "",\n                selectedCustomerId = null,\n                previousOutstanding = 0.0,'
)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
