content = """package com.example.model

import kotlinx.coroutines.flow.Flow
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class GroceryRepository(private val database: AppDatabase) {
    private val firestore = FirebaseFirestore.getInstance()
    private val externalScope = CoroutineScope(Dispatchers.IO)
    
    val allCustomers: Flow<List<Customer>> = database.customerDao().getAllCustomers()
    val allInvoices: Flow<List<Invoice>> = database.invoiceDao().getAllInvoices()
    val allItems: Flow<List<GroceryItem>> = database.groceryItemDao().getAllItems()
    val allPayments: Flow<List<Payment>> = database.paymentDao().getAllPayments()

    suspend fun insertCustomer(customer: Customer) {
        database.customerDao().insertCustomer(customer)
        externalScope.launch {
            try { firestore.collection("customers").document(customer.id).set(customer) } catch (e: Exception) {}
        }
    }
    
    suspend fun updateCustomer(customer: Customer) {
        database.customerDao().updateCustomer(customer)
        externalScope.launch {
            try { firestore.collection("customers").document(customer.id).set(customer) } catch (e: Exception) {}
        }
    }
    
    suspend fun insertInvoice(invoice: Invoice) {
        database.invoiceDao().insertInvoice(invoice)
        externalScope.launch {
            try { firestore.collection("invoices").document(invoice.invoiceId).set(invoice) } catch (e: Exception) {}
        }
    }
    
    suspend fun insertItem(item: GroceryItem) {
        database.groceryItemDao().insertItem(item)
        externalScope.launch {
            try { firestore.collection("inventory").document(item.id).set(item) } catch (e: Exception) {}
        }
    }
    
    suspend fun updateItem(item: GroceryItem) {
        database.groceryItemDao().updateItem(item)
        externalScope.launch {
            try { firestore.collection("inventory").document(item.id).set(item) } catch (e: Exception) {}
        }
    }
    
    suspend fun deleteItem(id: String) {
        database.groceryItemDao().deleteItem(id)
        externalScope.launch {
            try { firestore.collection("inventory").document(id).delete() } catch (e: Exception) {}
        }
    }
    
    suspend fun insertPayment(payment: Payment) {
        database.paymentDao().insertPayment(payment)
        externalScope.launch {
            try { firestore.collection("payments").document(payment.id).set(payment) } catch (e: Exception) {}
        }
    }
    
    fun syncFromFirebase() {
        try {
            firestore.collection("customers").get().addOnSuccessListener { result ->
                externalScope.launch {
                    for (document in result) {
                        try {
                            val customer = document.toObject(Customer::class.java)
                            database.customerDao().insertCustomer(customer)
                        } catch (e: Exception) {}
                    }
                }
            }
            firestore.collection("invoices").get().addOnSuccessListener { result ->
                externalScope.launch {
                    for (document in result) {
                        try {
                            val invoice = document.toObject(Invoice::class.java)
                            database.invoiceDao().insertInvoice(invoice)
                        } catch (e: Exception) {}
                    }
                }
            }
            firestore.collection("inventory").get().addOnSuccessListener { result ->
                externalScope.launch {
                    for (document in result) {
                        try {
                            val item = document.toObject(GroceryItem::class.java)
                            database.groceryItemDao().insertItem(item)
                        } catch (e: Exception) {}
                    }
                }
            }
            firestore.collection("payments").get().addOnSuccessListener { result ->
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
"""

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'w') as f:
    f.write(content)
