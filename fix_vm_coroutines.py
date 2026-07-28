import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

init_block = """    init {
        _uiState.update { it.copy(inventoryItems = defaultVeggieCatalog) }
        
        viewModelScope.launch {
            repository.allCustomers.collect { customers ->
                _uiState.update { it.copy(customers = customers) }
            }
        }
        viewModelScope.launch {
            repository.allInvoices.collect { invoices ->
                _uiState.update { it.copy(invoiceHistory = invoices) }
            }
        }
        viewModelScope.launch {
            repository.allItems.collect { items ->
                _uiState.update { it.copy(inventoryItems = if (items.isEmpty()) defaultVeggieCatalog else items) }
            }
        }
        viewModelScope.launch {
            repository.allPayments.collect { payments ->
                _uiState.update { it.copy(payments = payments) }
            }
        }
    }"""

content = re.sub(r'    init \{\n        _uiState.update \{ it.copy\(inventoryItems = defaultVeggieCatalog\) \}\n    \}', init_block, content)

# update addCustomer
add_customer = """    fun addCustomer(name: String, phone: String) {
        val newCustomer = Customer(
            id = "cust_${System.currentTimeMillis()}",
            name = name.trim(),
            phone = phone.trim(),
            balance = 0.0
        )
        viewModelScope.launch {
            repository.insertCustomer(newCustomer)
        }
    }"""
content = re.sub(r'    fun addCustomer\(name: String, phone: String\) \{.*?\n        \}\n    \}', add_customer, content, flags=re.DOTALL)

# update settleCustomerBalance
settle = """    fun settleCustomerBalance(customerId: String, amount: Double) {
        if (amount <= 0) return
        val payment = Payment(
            id = "pay_${System.currentTimeMillis()}",
            customerId = customerId,
            amount = amount
        )
        viewModelScope.launch {
            repository.insertPayment(payment)
            val customer = _uiState.value.customers.find { it.id == customerId }
            if (customer != null) {
                repository.updateCustomer(customer.copy(balance = customer.balance - amount))
            }
        }
    }"""
content = re.sub(r'    fun settleCustomerBalance\(customerId: String, amount: Double\) \{.*?\n        \}\n    \}', settle, content, flags=re.DOTALL)

# update generateInvoice
gen_invoice = """    fun generateInvoice(): Invoice {
        val state = _uiState.value
        val invNumber = state.editingInvoiceId ?: ("INV-" + (1000..9999).random())
        val invoice = Invoice(
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
        )
        
        viewModelScope.launch {
            repository.insertInvoice(invoice)
            
            val customerId = state.selectedCustomerId
            if (customerId != null) {
                val customer = state.customers.find { it.id == customerId }
                if (customer != null) {
                    repository.updateCustomer(customer.copy(balance = invoice.totalBalance))
                }
            }
        }

        _uiState.update {
            it.copy(
                currentInvoice = invoice,
                editingInvoiceId = null
            )
        }
        return invoice
    }"""
content = re.sub(r'    fun generateInvoice\(\): Invoice \{.*?\n        return invoice\n    \}', gen_invoice, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
