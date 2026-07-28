import re

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'r') as f:
    content = f.read()

sync_addition = """
            firestore.collection("settings").document("storeInfo").get().addOnSuccessListener { document ->
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
"""

content = content.replace('firestore.collection("customers").get().addOnSuccessListener { result ->', sync_addition + '\n            firestore.collection("customers").get().addOnSuccessListener { result ->')

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'w') as f:
    f.write(content)

