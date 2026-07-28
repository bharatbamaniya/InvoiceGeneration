package com.example.model

import kotlinx.coroutines.flow.Flow
import android.content.Context
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class GroceryRepository(private val database: AppDatabase, private val context: Context) {
    private val firestore = FirebaseFirestore.getInstance()
    private val externalScope = CoroutineScope(Dispatchers.IO)
    
    val allCustomers: Flow<List<Customer>> = database.customerDao().getAllCustomers()
    val allInvoices: Flow<List<Invoice>> = database.invoiceDao().getAllInvoices()
    val allItems: Flow<List<GroceryItem>> = database.groceryItemDao().getAllItems()
    val allPayments: Flow<List<Payment>> = database.paymentDao().getAllPayments()




    suspend fun clearLocalData() {
        kotlinx.coroutines.withContext(Dispatchers.IO) {
            database.clearAllTables()
        }
    }

    fun getStoreUid(): String? {
        val prefs = context.getSharedPreferences("store_settings", Context.MODE_PRIVATE)
        val uid = prefs.getString("store_uid", null)
        return if (uid.isNullOrBlank()) null else uid
    }
    
    fun setStoreUid(uid: String) {
        val prefs = context.getSharedPreferences("store_settings", Context.MODE_PRIVATE)
        prefs.edit().putString("store_uid", uid).apply()
        syncFromFirebase()
    }
    
    private fun getStoreDoc() = firestore.collection("stores").document(getStoreUid() ?: "default_store")

    fun saveStoreSettings(name: String, address: String, phone: String, owner: String, currency: String, swipeToDelete: Boolean) {
        val prefs = context.getSharedPreferences("store_settings", Context.MODE_PRIVATE)
        prefs.edit()
            .putString("storeName", name)
            .putString("storeAddress", address)
            .putString("storePhone", phone)
            .putString("ownerName", owner)
            .putString("currencySymbol", currency)
            .putBoolean("swipeToDelete", swipeToDelete)
            .apply()
            
        val map = mapOf(
            "storeName" to name,
            "storeAddress" to address,
            "storePhone" to phone,
            "ownerName" to owner,
            "currencySymbol" to currency,
            "swipeToDeleteEnabled" to swipeToDelete
        )
        externalScope.launch {
            try { getStoreDoc().set(map) } catch (e: Exception) {}
        }
    }
    
    fun getLocalStoreSettings(): Map<String, Any> {
        val prefs = context.getSharedPreferences("store_settings", Context.MODE_PRIVATE)
        return mapOf(
            "storeName" to prefs.getString("storeName", "Fresh Veggies Market") as Any,
            "storeAddress" to prefs.getString("storeAddress", "123 Main Market") as Any,
            "storePhone" to prefs.getString("storePhone", "+91 98765 43210") as Any,
            "ownerName" to prefs.getString("ownerName", "Owner Name") as Any,
            "currencySymbol" to prefs.getString("currencySymbol", "₹") as Any,
            "swipeToDelete" to prefs.getBoolean("swipeToDelete", true) as Any
        )
    }

    suspend fun insertCustomer(customer: Customer) {
        database.customerDao().insertCustomer(customer)
        externalScope.launch {
            try { getStoreDoc().collection("customers").document(customer.id).set(customer) } catch (e: Exception) {}
        }
    }
    
    suspend fun updateCustomer(customer: Customer) {
        database.customerDao().updateCustomer(customer)
        externalScope.launch {
            try { getStoreDoc().collection("customers").document(customer.id).set(customer) } catch (e: Exception) {}
        }
    }
    
    suspend fun insertInvoice(invoice: Invoice) {
        database.invoiceDao().insertInvoice(invoice)
        externalScope.launch {
            try { getStoreDoc().collection("invoices").document(invoice.invoiceId).set(invoice) } catch (e: Exception) {}
        }
    }
    
    suspend fun insertItem(item: GroceryItem) {
        database.groceryItemDao().insertItem(item)
        externalScope.launch {
            try { getStoreDoc().collection("inventory").document(item.id).set(item) } catch (e: Exception) {}
        }
    }
    
    suspend fun updateItem(item: GroceryItem) {
        database.groceryItemDao().updateItem(item)
        externalScope.launch {
            try { getStoreDoc().collection("inventory").document(item.id).set(item) } catch (e: Exception) {}
        }
    }
    
    suspend fun deleteItem(id: String) {
        database.groceryItemDao().deleteItem(id)
        externalScope.launch {
            try { getStoreDoc().collection("inventory").document(id).delete() } catch (e: Exception) {}
        }
    }
    
    suspend fun insertPayment(payment: Payment) {
        database.paymentDao().insertPayment(payment)
        externalScope.launch {
            try { getStoreDoc().collection("payments").document(payment.id).set(payment) } catch (e: Exception) {}
        }
    }
    
    fun syncFromFirebase() {
        try {
            
            getStoreDoc().get().addOnSuccessListener { document ->
                if (document != null && document.exists()) {
                    val name = document.getString("storeName") ?: "Fresh Veggies Market"
                    val address = document.getString("storeAddress") ?: ""
                    val phone = document.getString("storePhone") ?: ""
                    val owner = document.getString("ownerName") ?: "Owner Name"
                    val currency = document.getString("currencySymbol") ?: "₹"
                    val swipeToDelete = document.getBoolean("swipeToDeleteEnabled") ?: true
                    
                    val prefs = context.getSharedPreferences("store_settings", Context.MODE_PRIVATE)
                    prefs.edit()
                        .putString("storeName", name)
                        .putString("storeAddress", address)
                        .putString("storePhone", phone)
                        .putString("ownerName", owner)
                        .putString("currencySymbol", currency)
                        .putBoolean("swipeToDelete", swipeToDelete)
                        .apply()
                }
            }

            getStoreDoc().collection("customers").get().addOnSuccessListener { result ->
                externalScope.launch {
                    for (document in result) {
                        try {
                            val customer = document.toObject(Customer::class.java)
                            database.customerDao().insertCustomer(customer)
                        } catch (e: Exception) {}
                    }
                }
            }
            getStoreDoc().collection("invoices").get().addOnSuccessListener { result ->
                externalScope.launch {
                    for (document in result) {
                        try {
                            val invoice = document.toObject(Invoice::class.java)
                            database.invoiceDao().insertInvoice(invoice)
                        } catch (e: Exception) {}
                    }
                }
            }
            getStoreDoc().collection("inventory").get().addOnSuccessListener { result ->
                externalScope.launch {
                    for (document in result) {
                        try {
                            val item = document.toObject(GroceryItem::class.java)
                            database.groceryItemDao().insertItem(item)
                        } catch (e: Exception) {}
                    }
                }
            }
            getStoreDoc().collection("payments").get().addOnSuccessListener { result ->
                externalScope.launch {
                    for (document in result) {
                        try {
                            val payment = document.toObject(Payment::class.java)
                            database.paymentDao().insertPayment(payment)
                        } catch (e: Exception) {}
                    }
                }
            }
        } catch (e: Exception) {}
    }
}
