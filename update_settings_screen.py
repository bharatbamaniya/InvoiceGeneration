import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'onUpdateStoreSettings: (name: String, address: String, phone: String, symbol: String) -> Unit,',
    'onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, symbol: String) -> Unit,'
)

content = content.replace(
    'var storePhone by remember { mutableStateOf(state.storePhone) }',
    'var storePhone by remember { mutableStateOf(state.storePhone) }\n    var ownerName by remember { mutableStateOf(state.ownerName) }'
)

new_fields = """                OutlinedTextField(
                    value = storePhone,
                    onValueChange = { storePhone = it },
                    label = { Text("Store Phone") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = ownerName,
                    onValueChange = { ownerName = it },
                    label = { Text("Owner Name") },
                    modifier = Modifier.fillMaxWidth()
                )"""

content = content.replace(
    '                OutlinedTextField(\n                    value = storePhone,\n                    onValueChange = { storePhone = it },\n                    label = { Text("Store Phone") },\n                    modifier = Modifier.fillMaxWidth()\n                )',
    new_fields
)

content = content.replace(
    'onUpdateStoreSettings(storeName, storeAddress, storePhone, currencySymbol)',
    'onUpdateStoreSettings(storeName, storeAddress, storePhone, ownerName, currencySymbol)'
)

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(content)
