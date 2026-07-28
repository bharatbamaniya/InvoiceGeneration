import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("enum class AppScreen {", "enum class AppScreen {\n    HOME,\n    SETTINGS,")
content = content.replace("var currentScreen by remember { mutableStateOf(AppScreen.CUSTOMERS) }", "var currentScreen by remember { mutableStateOf(AppScreen.HOME) }")
content = content.replace("BackHandler(enabled = currentScreen != AppScreen.CUSTOMERS) {", "BackHandler(enabled = currentScreen != AppScreen.HOME) {")
content = content.replace("else -> currentScreen = AppScreen.CUSTOMERS", "else -> currentScreen = AppScreen.HOME")
content = content.replace("AppScreen.CUSTOMER_DETAIL -> currentScreen = AppScreen.CUSTOMERS", "AppScreen.CUSTOMER_DETAIL -> currentScreen = AppScreen.CUSTOMERS")
content = content.replace("AppScreen.INVOICE_HISTORY -> currentScreen = AppScreen.CUSTOMERS", "AppScreen.INVOICE_HISTORY -> currentScreen = AppScreen.HOME")
content = content.replace("AppScreen.CHECKOUT -> currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.CUSTOMERS", "AppScreen.CHECKOUT -> currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.HOME")
content = content.replace("AppScreen.INVOICE_DETAIL -> currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.HOME", "AppScreen.INVOICE_DETAIL -> currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.HOME")
content = content.replace("AppScreen.MANAGE_ITEMS -> currentScreen = AppScreen.CHECKOUT", "AppScreen.MANAGE_ITEMS -> currentScreen = AppScreen.CHECKOUT")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
