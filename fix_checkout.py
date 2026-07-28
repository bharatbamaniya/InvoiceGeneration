import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main_content = f.read()

# I will fix the CheckoutScreen's lambda specifically
checkout_old = "onUpdateStoreSettings = { name, address, phone, owner, symbol, swipe -> viewModel.updateStoreSettings(name, address, phone, owner, symbol, swipe) },\n                onGenerateInvoice = {"
checkout_new = "onUpdateStoreSettings = { name, address, phone, owner, symbol -> viewModel.updateStoreSettings(name, address, phone, owner, symbol) },\n                onGenerateInvoice = {"
main_content = main_content.replace(checkout_old, checkout_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main_content)

