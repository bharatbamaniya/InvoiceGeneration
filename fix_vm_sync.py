import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

sync_method = """    fun syncData() {
        viewModelScope.launch {
            repository.syncFromFirebase()
        }
    }
"""

content = content.replace("    fun login(storeUid: String) {", sync_method + "\n    fun login(storeUid: String) {")

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
