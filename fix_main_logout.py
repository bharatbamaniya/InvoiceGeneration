import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("                        onUpdateStoreSettings = { name, address, phone, owner, swipe -> viewModel.updateStoreSettings(name, address, phone, owner, swipe) },\n                        onBack = { currentScreen = AppScreen.HOME }\n                    )", "                        onUpdateStoreSettings = { name, address, phone, owner, swipe -> viewModel.updateStoreSettings(name, address, phone, owner, swipe) },\n                        onLogout = { viewModel.logout() },\n                        onBack = { currentScreen = AppScreen.HOME }\n                    )")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

