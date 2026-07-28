import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

# Add customer management functions
customer_funcs = """

    fun addCustomer(name: String, phone: String) {
        val newCustomer = Customer(
            id = "cust_${System.currentTimeMillis()}",
            name = name.trim(),
            phone = phone.trim(),
            balance = 0.0
        )
        _uiState.update { state ->
            state.copy(customers = state.customers + newCustomer)
        }
    }

    fun selectCustomer(customerId: String?) {
        _uiState.update { state ->
            val customer = state.customers.find { it.id == customerId }
            state.copy(
                selectedCustomerId = customerId,
                customerName = customer?.name ?: "",
                customerPhone = customer?.phone ?: "",
                previousOutstanding = customer?.balance ?: 0.0
            )
        }
    }

    fun settleCustomerBalance(customerId: String, amount: Double) {
        if (amount <= 0) return
        val payment = Payment(
            id = "pay_${System.currentTimeMillis()}",
            customerId = customerId,
            amount = amount
        )
        _uiState.update { state ->
            val updatedCustomers = state.customers.map {
                if (it.id == customerId) it.copy(balance = it.balance - amount) else it
            }
            state.copy(
                customers = updatedCustomers,
                payments = state.payments + payment
            )
        }
    }
"""

content = content.replace("fun generateInvoice(): Invoice {", customer_funcs + "\n    fun generateInvoice(): Invoice {")

# In generateInvoice, we need to add customerId and update customer balance.
# Look for Invoice( ... )
old_invoice_creation = """val invoice = Invoice(
            invoiceId = invNumber,
            storeName = state.storeName,
            storeAddress = state.storeAddress,
            storePhone = state.storePhone,
            ownerName = state.ownerName,
            customerName = state.customerName.ifBlank { "Walk-in Customer" },
            customerPhone = state.customerPhone,
            items = state.cartItems,
            previousOutstanding = state.previousOutstanding,
            cashReceived = state.cashReceived,
            currencySymbol = state.currencySymbol
        )"""

new_invoice_creation = """val invoice = Invoice(
            invoiceId = invNumber,
            storeName = state.storeName,
            storeAddress = state.storeAddress,
            storePhone = state.storePhone,
            ownerName = state.ownerName,
            customerName = state.customerName.ifBlank { "Walk-in Customer" },
            customerPhone = state.customerPhone,
            customerId = state.selectedCustomerId,
            items = state.cartItems,
            previousOutstanding = state.previousOutstanding,
            cashReceived = state.cashReceived,
            currencySymbol = state.currencySymbol
        )"""

content = content.replace(old_invoice_creation, new_invoice_creation)

old_update = """        _uiState.update {
            val updatedHistory = if (state.editingInvoiceId != null) {
                it.invoiceHistory.map { inv -> if (inv.invoiceId == invNumber) invoice else inv }
            } else {
                listOf(invoice) + it.invoiceHistory
            }
            it.copy(
                currentInvoice = invoice,
                invoiceHistory = updatedHistory,
                editingInvoiceId = null
            )
        }"""

new_update = """        _uiState.update {
            val updatedHistory = if (state.editingInvoiceId != null) {
                it.invoiceHistory.map { inv -> if (inv.invoiceId == invNumber) invoice else inv }
            } else {
                listOf(invoice) + it.invoiceHistory
            }
            
            val updatedCustomers = if (state.selectedCustomerId != null) {
                it.customers.map { cust ->
                    if (cust.id == state.selectedCustomerId) {
                        // The balance becomes the new totalBalance.
                        cust.copy(balance = invoice.totalBalance)
                    } else cust
                }
            } else it.customers

            it.copy(
                currentInvoice = invoice,
                invoiceHistory = updatedHistory,
                customers = updatedCustomers,
                editingInvoiceId = null
            )
        }"""

content = content.replace(old_update, new_update)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
