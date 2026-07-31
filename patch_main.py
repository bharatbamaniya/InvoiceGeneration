import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# Fix CustomerDetailScreen invocation
# Old: 
# payments = uiState.payments.filter { it.customerId == customer.id },
# currencySymbol = uiState.currencySymbol,
# onBack = { currentScreen = AppScreen.CUSTOMERS },
# onNewInvoice = { ... },
# onSettleBalance = { amount, remark -> viewModel.settleCustomerBalance(customer.id, amount, remark) },
# onViewInvoice = { invoice -> ... }
code = re.sub(
    r'payments = uiState\.payments\.filter \{.*?\},',
    '',
    code,
    flags=re.DOTALL
)

code = re.sub(
    r'onSettleBalance = \{ amount, remark -> viewModel\.settleCustomerBalance\(customer\.id, amount, remark\) \},',
    r'onSettleBalance = { cust, amount -> viewModel.settleCustomerBalance(cust.id, amount, "Settled from detail") },',
    code,
    flags=re.DOTALL
)

code = re.sub(
    r'onViewInvoice = \{ invoice ->.*?\}',
    r'',
    code,
    flags=re.DOTALL
)

# Fix InvoiceDetailScreen invocation
# Old: onNewSale = { ... }
code = re.sub(
    r'onNewSale = \{',
    r'onHome = {\nviewModel.resetInvoice()\nselectedInvoiceForView = null\ncurrentScreen = AppScreen.HOME\n},\nonNewSale = {',
    code,
    flags=re.DOTALL
)

# Fix InvoiceHistoryScreen invocation
# Old: 
# invoices = uiState.invoiceHistory,
# onSelectInvoice = { invoice -> ... },
# onEditInvoice = { invoice -> ... },
# onBack = { currentScreen = AppScreen.HOME }
code = re.sub(
    r'onSelectInvoice = \{ invoice ->',
    r'currencySymbol = uiState.currencySymbol,\nonInvoiceClick = { invoice ->',
    code,
    flags=re.DOTALL
)
code = re.sub(
    r'onEditInvoice = \{ invoice ->.*?\},',
    r'',
    code,
    flags=re.DOTALL
)


with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)

