import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("    onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, symbol: String, swipeToDelete: Boolean) -> Unit,", "    onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, swipeToDelete: Boolean) -> Unit,")

content = content.replace("    var currencySymbol by remember { mutableStateOf(state.currencySymbol) }\n", "")

currency_field = """                OutlinedTextField(
                    value = currencySymbol,
                    onValueChange = { currencySymbol = it },
                    label = { Text("Currency Symbol") },
                    modifier = Modifier.fillMaxWidth()
                )"""
content = content.replace(currency_field, "")

content = content.replace("onUpdateStoreSettings(storeName, storeAddress, storePhone, ownerName, currencySymbol, swipeToDeleteEnabled)", "onUpdateStoreSettings(storeName, storeAddress, storePhone, ownerName, swipeToDeleteEnabled)")

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(content)
    
