with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

import re

old_block = re.search(r'InvoiceDetailScreen\([^)]+\)', content, re.DOTALL).group(0)

new_block = """InvoiceDetailScreen(
                    invoice = activeInvoice,
                    onBackToCheckout = { currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.CHECKOUT },
                    onNewSale = {
                        val prevCustId = uiState.selectedCustomerId
                        viewModel.resetInvoice()
                        selectedInvoiceForView = null
                        viewModel.selectCustomer(prevCustId)
                        currentScreen = if (prevCustId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.CHECKOUT
                    },
                    onEditInvoice = {
                        viewModel.loadInvoiceForEditing(activeInvoice)
                        selectedInvoiceForView = null
                        currentScreen = AppScreen.CHECKOUT
                    }
                )"""

content = content.replace(old_block, new_block)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
