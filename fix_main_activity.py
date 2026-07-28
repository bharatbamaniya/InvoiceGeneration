import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_call = """                CustomerDetailScreen(
                    customer = customer,
                    invoices = uiState.invoiceHistory.filter { it.customerId == customer.id },
                    currencySymbol = uiState.currencySymbol,"""

new_call = """                CustomerDetailScreen(
                    customer = customer,
                    invoices = uiState.invoiceHistory.filter { it.customerId == customer.id },
                    payments = uiState.payments.filter { it.customerId == customer.id },
                    currencySymbol = uiState.currencySymbol,"""

content = content.replace(old_call, new_call)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
