import re

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'r') as f:
    content = f.read()

# Add getStoreUid / setStoreUid
auth_funcs = """
    fun getStoreUid(): String? {
        val prefs = context.getSharedPreferences("store_settings", Context.MODE_PRIVATE)
        return prefs.getString("store_uid", null)
    }
    
    fun setStoreUid(uid: String) {
        val prefs = context.getSharedPreferences("store_settings", Context.MODE_PRIVATE)
        prefs.edit().putString("store_uid", uid).apply()
        syncFromFirebase()
    }
    
    private fun getStoreDoc() = firestore.collection("stores").document(getStoreUid() ?: "default_store")
"""

content = content.replace("    fun saveStoreSettings(", auth_funcs + "\n    fun saveStoreSettings(")

# Replace firestore.collection("...") with getStoreDoc().collection("...")
content = content.replace('firestore.collection("settings").document("storeInfo")', 'getStoreDoc()')
content = content.replace('firestore.collection("customers")', 'getStoreDoc().collection("customers")')
content = content.replace('firestore.collection("invoices")', 'getStoreDoc().collection("invoices")')
content = content.replace('firestore.collection("inventory")', 'getStoreDoc().collection("inventory")')
content = content.replace('firestore.collection("payments")', 'getStoreDoc().collection("payments")')

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'w') as f:
    f.write(content)

