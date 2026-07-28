import re

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'r') as f:
    content = f.read()

# Add Context import if needed
if "import android.content.Context" not in content:
    content = content.replace("import com.google.firebase.firestore.FirebaseFirestore", "import android.content.Context\nimport com.google.firebase.firestore.FirebaseFirestore")

# Change constructor
content = content.replace("class GroceryRepository(private val database: AppDatabase) {", "class GroceryRepository(private val database: AppDatabase, private val context: Context) {")

# Add StoreSettings function
settings_funcs = """
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
            try { firestore.collection("settings").document("storeInfo").set(map) } catch (e: Exception) {}
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
"""

content = content.replace("    suspend fun insertCustomer", settings_funcs + "\n    suspend fun insertCustomer")

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'w') as f:
    f.write(content)

