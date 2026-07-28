import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, symbol: String) -> Unit,',
    'onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, symbol: String, swipeToDelete: Boolean) -> Unit,'
)

content = content.replace(
    'var swipeToDeleteEnabled by remember { mutableStateOf(true) }',
    'var swipeToDeleteEnabled by remember { mutableStateOf(state.swipeToDeleteEnabled) }'
)

content = content.replace(
    'onUpdateStoreSettings(storeName, storeAddress, storePhone, ownerName, currencySymbol)',
    'onUpdateStoreSettings(storeName, storeAddress, storePhone, ownerName, currencySymbol, swipeToDeleteEnabled)'
)

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(content)


with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main_content = f.read()

main_content = main_content.replace(
    'onUpdateStoreSettings = viewModel::updateStoreSettings,',
    'onUpdateStoreSettings = { name, address, phone, owner, symbol, swipe -> viewModel.updateStoreSettings(name, address, phone, owner, symbol, swipe) },'
)
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main_content)

