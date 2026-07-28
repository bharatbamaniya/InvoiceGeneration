import re

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'r') as f:
    content = f.read()

clear_func = """
    suspend fun clearLocalData() {
        database.clearAllTables()
    }
"""

content = content.replace("    fun getStoreUid(): String? {", clear_func + "\n    fun getStoreUid(): String? {")

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'w') as f:
    f.write(content)
