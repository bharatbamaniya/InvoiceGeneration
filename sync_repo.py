with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'r') as f:
    content = f.read()

sync_code = """
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

content = content.replace("}\n", sync_code)

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'w') as f:
    f.write(content)
