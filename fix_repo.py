with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'r') as f:
    content = f.read()

imports = """package com.example.model

import kotlinx.coroutines.flow.Flow
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
"""

content = content.replace("package com.example.model\n\nimport kotlinx.coroutines.flow.Flow", imports)

firebase = """
    private val firestore = FirebaseFirestore.getInstance()
    private val externalScope = CoroutineScope(Dispatchers.IO)
"""

content = content.replace("class GroceryRepository(private val database: AppDatabase) {", "class GroceryRepository(private val database: AppDatabase) {" + firebase)

insert_cust = """    suspend fun insertCustomer(customer: Customer) {
        database.customerDao().insertCustomer(customer)
        externalScope.launch {
            try { firestore.collection("customers").document(customer.id).set(customer) } catch (e: Exception) {}
        }
    }"""
content = content.replace("    suspend fun insertCustomer(customer: Customer) = database.customerDao().insertCustomer(customer)", insert_cust)

update_cust = """    suspend fun updateCustomer(customer: Customer) {
        database.customerDao().updateCustomer(customer)
        externalScope.launch {
            try { firestore.collection("customers").document(customer.id).set(customer) } catch (e: Exception) {}
        }
    }"""
content = content.replace("    suspend fun updateCustomer(customer: Customer) = database.customerDao().updateCustomer(customer)", update_cust)

insert_inv = """    suspend fun insertInvoice(invoice: Invoice) {
        database.invoiceDao().insertInvoice(invoice)
        externalScope.launch {
            try { firestore.collection("invoices").document(invoice.invoiceId).set(invoice) } catch (e: Exception) {}
        }
    }"""
content = content.replace("    suspend fun insertInvoice(invoice: Invoice) = database.invoiceDao().insertInvoice(invoice)", insert_inv)

insert_item = """    suspend fun insertItem(item: GroceryItem) {
        database.groceryItemDao().insertItem(item)
        externalScope.launch {
            try { firestore.collection("inventory").document(item.id).set(item) } catch (e: Exception) {}
        }
    }"""
content = content.replace("    suspend fun insertItem(item: GroceryItem) = database.groceryItemDao().insertItem(item)", insert_item)

update_item = """    suspend fun updateItem(item: GroceryItem) {
        database.groceryItemDao().updateItem(item)
        externalScope.launch {
            try { firestore.collection("inventory").document(item.id).set(item) } catch (e: Exception) {}
        }
    }"""
content = content.replace("    suspend fun updateItem(item: GroceryItem) = database.groceryItemDao().updateItem(item)", update_item)

delete_item = """    suspend fun deleteItem(id: String) {
        database.groceryItemDao().deleteItem(id)
        externalScope.launch {
            try { firestore.collection("inventory").document(id).delete() } catch (e: Exception) {}
        }
    }"""
content = content.replace("    suspend fun deleteItem(id: String) = database.groceryItemDao().deleteItem(id)", delete_item)

insert_pay = """    suspend fun insertPayment(payment: Payment) {
        database.paymentDao().insertPayment(payment)
        externalScope.launch {
            try { firestore.collection("payments").document(payment.id).set(payment) } catch (e: Exception) {}
        }
    }"""
content = content.replace("    suspend fun insertPayment(payment: Payment) = database.paymentDao().insertPayment(payment)", insert_pay)

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'w') as f:
    f.write(content)
