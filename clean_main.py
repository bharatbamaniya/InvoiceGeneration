import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Remove the arguments from CheckoutScreen invocation in MainActivity
content = content.replace("                        onUpdateCustomerName = viewModel::updateCustomerName,\n", "")
content = content.replace("                        onUpdateCustomerPhone = viewModel::updateCustomerPhone,\n", "")
content = content.replace("                        onUpdateStoreSettings = { name, address, phone, owner, symbol -> viewModel.updateStoreSettings(name, address, phone, owner, symbol, uiState.swipeToDeleteEnabled) },\n", "")
content = content.replace("                        onOpenHistory = {\n                            currentScreen = AppScreen.INVOICE_HISTORY\n                        },\n", "")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

