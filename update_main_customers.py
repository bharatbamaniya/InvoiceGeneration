import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("onSkipToCheckout = {\n                            viewModel.selectCustomer(null)\n                            currentScreen = AppScreen.CHECKOUT\n                        }", "")

old_on_new_invoice_home = """                        onNewInvoice = {
                            viewModel.selectCustomer(null)
                            currentScreen = AppScreen.CHECKOUT 
                        },"""
new_on_new_invoice_home = """                        onNewInvoice = {
                            viewModel.clearCart()
                            currentScreen = AppScreen.CUSTOMERS 
                        },"""
content = content.replace(old_on_new_invoice_home, new_on_new_invoice_home)

old_on_new_invoice_cust = """                            onNewInvoice = { currentScreen = AppScreen.CHECKOUT },"""
new_on_new_invoice_cust = """                            onNewInvoice = { 
                                viewModel.clearCart()
                                currentScreen = AppScreen.CHECKOUT 
                            },"""
content = content.replace(old_on_new_invoice_cust, new_on_new_invoice_cust)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
