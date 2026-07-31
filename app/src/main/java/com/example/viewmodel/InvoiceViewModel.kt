package com.example.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.model.GroceryRepository
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn
import androidx.lifecycle.ViewModelProvider
import com.example.model.GroceryItem
import com.example.model.Invoice
import com.example.model.InvoiceItem
import com.example.model.Customer
import com.example.model.Payment
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import java.util.UUID

data class InvoiceUiState(
    val storeName: String = "Fresh Veggies Market",
    val storeAddress: String = "123 Main Market",
    val storePhone: String = "+91 98765 43210",
    val ownerName: String = "Owner Name",
    val currencySymbol: String = "₹",
    val customerName: String = "",
    val customerPhone: String = "",
    val searchQuery: String = "",
    val cartItems: List<InvoiceItem> = emptyList(),
    val previousOutstanding: Double = 0.0,
    val cashReceived: Double = 0.0,
    val currentInvoice: Invoice? = null,
    val invoiceHistory: List<Invoice> = emptyList(),
    val customers: List<Customer> = emptyList(),
    val selectedCustomerId: String? = null,
    val payments: List<Payment> = emptyList(),
    val inventoryItems: List<GroceryItem> = emptyList(),
    val editingInvoiceId: String? = null,
    val swipeToDeleteEnabled: Boolean = true,
    val isAuthenticated: Boolean = false,
    val storeUid: String = ""
)

class InvoiceViewModel(private val repository: GroceryRepository) : ViewModel() {

    private val _uiState = MutableStateFlow(InvoiceUiState())
    val uiState: StateFlow<InvoiceUiState> = _uiState.asStateFlow()

    // Default Vegetable Catalog
    val defaultVeggieCatalog = listOf(
        GroceryItem("v1", "Potato", 30.0, "kg", "🥔"),
        GroceryItem("v2", "Onion", 40.0, "kg", "🧅"),
        GroceryItem("v3", "Tomato", 50.0, "kg", "🍅"),
        GroceryItem("v4", "Cabbage", 30.0, "pc", "🥬"),
        GroceryItem("v5", "Cauliflower", 40.0, "pc", "🥦"),
        GroceryItem("v6", "Carrot", 60.0, "kg", "🥕"),
        GroceryItem("v7", "Spinach", 20.0, "bunch", "🥬"),
        GroceryItem("v8", "Green Peas", 80.0, "kg", "🫛"),
        GroceryItem("v9", "Cucumber", 30.0, "kg", "🥒"),
        GroceryItem("v10", "Capsicum", 60.0, "kg", "🫑"),
        GroceryItem("v11", "Eggplant", 40.0, "kg", "🍆"),
        GroceryItem("v12", "Garlic", 120.0, "kg", "🧄"),
        GroceryItem("v13", "Ginger", 150.0, "kg", "🫚"),
        GroceryItem("v14", "Green Chili", 100.0, "kg", "🌶️"),
        GroceryItem("v15", "Coriander", 15.0, "bunch", "🌿"),
        GroceryItem("v16", "Mint", 10.0, "bunch", "🌿"),
        GroceryItem("v17", "Radish", 20.0, "kg", "🥕"),
        GroceryItem("v18", "Bitter Gourd", 50.0, "kg", "🥒"),
        GroceryItem("v19", "Bottle Gourd", 25.0, "pc", "🥒"),
        GroceryItem("v20", "Pumpkin", 40.0, "kg", "🎃")
    )

    init {
        val localSettings = repository.getLocalStoreSettings()
        val uid = repository.getStoreUid()
        _uiState.update { it.copy(isAuthenticated = uid != null, storeUid = uid ?: "") }
        _uiState.update { 
            it.copy(
                storeName = localSettings["storeName"] as String,
                storeAddress = localSettings["storeAddress"] as String,
                storePhone = localSettings["storePhone"] as String,
                ownerName = localSettings["ownerName"] as String,
                currencySymbol = localSettings["currencySymbol"] as String,
                swipeToDeleteEnabled = localSettings["swipeToDelete"] as Boolean
            )
        }

        repository.syncFromFirebase()
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
                if (items.isEmpty()) {
                    defaultVeggieCatalog.forEach { repository.insertItem(it) }
                    _uiState.update { it.copy(inventoryItems = defaultVeggieCatalog) }
                } else {
                    _uiState.update { it.copy(inventoryItems = items) }
                }
            }
        }
        viewModelScope.launch {
            repository.allPayments.collect { payments ->
                _uiState.update { it.copy(payments = payments) }
            }
        }
    }


    fun syncData() {
        viewModelScope.launch {
            repository.syncFromFirebase()
        }
    }

    fun login(storeUid: String) {
        if (storeUid.isNotBlank()) {
            viewModelScope.launch {
                repository.clearLocalData()
                repository.setStoreUid(storeUid)
                _uiState.update { it.copy(isAuthenticated = true, storeUid = storeUid) }
            }
        }
    }
    

    
    fun logout() {
        viewModelScope.launch {
            repository.clearLocalData()
            repository.setStoreUid("")
            _uiState.update { 
                it.copy(
                    isAuthenticated = false, 
                    storeUid = "",
                    customers = emptyList(),
                    invoiceHistory = emptyList(),
                    inventoryItems = defaultVeggieCatalog,
                    payments = emptyList()
                ) 
            }
        }
    }

    fun updateCustomerName(name: String) {
        _uiState.update { it.copy(customerName = name) }
    }

    fun updateCustomerPhone(phone: String) {
        _uiState.update { it.copy(customerPhone = phone) }
    }

    fun updateSearchQuery(query: String) {
        _uiState.update { it.copy(searchQuery = query) }
    }

    fun updatePreviousOutstanding(amount: Double) {
        _uiState.update { it.copy(previousOutstanding = amount) }
    }

    fun updateCashReceived(amount: Double) {
        _uiState.update { it.copy(cashReceived = amount) }
    }

    fun updateStoreSettings(name: String, address: String, phone: String, owner: String, swipeToDelete: Boolean = true) {
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
    }

    /**
     * Add 1 unit of item to cart or increment existing
     */
    fun setCartItem(item: GroceryItem, quantity: Double, price: Double) {
        _uiState.update { state ->
            val existingIndex = state.cartItems.indexOfFirst { it.item.id == item.id }
            val updatedCart = if (existingIndex >= 0) {
                state.cartItems.mapIndexed { index, invoiceItem ->
                    if (index == existingIndex) {
                        invoiceItem.copy(
                            quantity = quantity,
                            customPrice = price
                        )
                    } else invoiceItem
                }
            } else {
                state.cartItems + InvoiceItem(item = item, quantity = quantity, customPrice = price)
            }
            state.copy(cartItems = updatedCart)
        }
    }

    fun addItemToCart(item: GroceryItem, customPrice: Double? = null) {
        _uiState.update { state ->
            val existingIndex = state.cartItems.indexOfFirst { it.item.id == item.id }
            val updatedCart = if (existingIndex >= 0) {
                state.cartItems.mapIndexed { index, invoiceItem ->
                    if (index == existingIndex) {
                        invoiceItem.copy(
                            quantity = invoiceItem.quantity + 1.0,
                            customPrice = customPrice ?: invoiceItem.customPrice
                        )
                    } else invoiceItem
                }
            } else {
                state.cartItems + InvoiceItem(item = item, quantity = 1.0, customPrice = customPrice)
            }
            state.copy(cartItems = updatedCart)
        }
    }

    /**
     * Decrement unit count of item or remove if 0
     */
    fun decrementCartItem(itemId: String) {
        _uiState.update { state ->
            val updatedCart = state.cartItems.mapNotNull { invoiceItem ->
                if (invoiceItem.item.id == itemId) {
                    if (invoiceItem.quantity > 1.0) {
                        invoiceItem.copy(quantity = invoiceItem.quantity - 1.0)
                    } else null
                } else invoiceItem
            }
            state.copy(cartItems = updatedCart)
        }
    }

    fun removeCartItem(itemId: String) {
        _uiState.update { state ->
            state.copy(cartItems = state.cartItems.filterNot { it.item.id == itemId })
        }
    }

    fun clearCart() {
        _uiState.update { it.copy(cartItems = emptyList()) }
    }

    fun editCartItemPrice(itemId: String, newPrice: Double) {
        _uiState.update { state ->
            val updatedCart = state.cartItems.map {
                if (it.item.id == itemId) it.copy(customPrice = newPrice) else it
            }
            state.copy(cartItems = updatedCart)
        }
    }

    fun editCartItemQuantity(itemId: String, newQty: Double) {
        _uiState.update { state ->
            val updatedCart = state.cartItems.mapNotNull {
                if (it.item.id == itemId) {
                    if (newQty > 0) it.copy(quantity = newQty) else null
                } else it
            }
            state.copy(cartItems = updatedCart)
        }
    }

    /**
     * Add custom unlisted item directly to quick list and cart
     */
    fun addCustomItem(name: String, price: Double, unit: String = "kg") {
        if (name.isBlank() || price <= 0.0) return

        val newItem = GroceryItem(
            id = "custom_${System.currentTimeMillis()}",
            name = name.trim(),
            price = price,
            unit = unit,
            iconEmoji = "📦"

        )

        viewModelScope.launch {
            repository.insertItem(newItem)
        }
        addItemToCart(newItem)
    }

    /**
     * Inventory management
     */
    fun addInventoryItem(name: String, price: Double, unit: String, iconEmoji: String = "") {
        val newItem = GroceryItem(
            id = "item_${System.currentTimeMillis()}",
            name = name.trim(),
            price = price,
            unit = unit,
            iconEmoji = iconEmoji,

        )
        viewModelScope.launch {
            repository.insertItem(newItem)
        }
    }

    fun updateInventoryItem(updatedItem: GroceryItem) {
        viewModelScope.launch {
            repository.updateItem(updatedItem)
        }
    }

    fun deleteInventoryItem(itemId: String) {
        _uiState.update { state ->
            state.copy(
                inventoryItems = state.inventoryItems.filter { it.id != itemId },
                cartItems = state.cartItems.filter { it.item.id != itemId }
            )
        }
    }

    /**
     * Load an invoice to edit it
     */
    fun loadInvoiceForEditing(invoice: Invoice) {
        _uiState.update { state ->
            state.copy(
                customerName = if (invoice.customerName == "Walk-in Customer") "" else invoice.customerName,
                customerPhone = invoice.customerPhone,
                cartItems = invoice.items,
                previousOutstanding = invoice.previousOutstanding,
                cashReceived = invoice.cashReceived,
                currencySymbol = invoice.currencySymbol,
                editingInvoiceId = invoice.invoiceId
            )
        }
    }

    /**
     * Generate the current invoice object
     */
    

    fun addCustomer(name: String, phone: String) {
        val newCustomer = Customer(
            id = "cust_${System.currentTimeMillis()}",
            name = name.trim(),
            phone = phone.trim(),
            balance = 0.0
        )
        viewModelScope.launch {
            repository.insertCustomer(newCustomer)
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

    fun settleCustomerBalance(customerId: String, amount: Double, remark: String = "") {
        if (amount <= 0) return
        val payment = Payment(
            id = "pay_${System.currentTimeMillis()}",
            customerId = customerId,
            amount = amount,
            remark = remark
        )
        viewModelScope.launch {
            repository.insertPayment(payment)
            val customer = _uiState.value.customers.find { it.id == customerId }
            if (customer != null) {
                repository.updateCustomer(customer.copy(balance = customer.balance - amount))
            }
        }
    }

    fun generateInvoice(): Invoice {
        val state = _uiState.value
        val invNumber = state.editingInvoiceId ?: run {
            val maxId = state.invoiceHistory.maxOfOrNull { 
                it.invoiceId.removePrefix("INV-").toIntOrNull() ?: 0 
            } ?: 0
            "INV-" + (maxId + 1).toString().padStart(4, '0')
        }
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
    }

    fun resetInvoice() {
        _uiState.update {
            it.copy(
                cartItems = emptyList(),
                customerName = "",
                customerPhone = "",
                selectedCustomerId = null,
                previousOutstanding = 0.0,
                cashReceived = 0.0,
                currentInvoice = null,
                editingInvoiceId = null
            )
        }
    }
}
