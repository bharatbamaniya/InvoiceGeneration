import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

old_code = """                            onSettleBalance = { cust, amount -> viewModel.settleCustomerBalance(cust.id, amount, "Settled from detail") },"""
new_code = """                            onSettleBalance = { cust, amount -> viewModel.settleCustomerBalance(cust.id, amount, "Settled from detail") },
                            onEditInvoice = { invoice -> 
                                viewModel.loadInvoiceForEditing(invoice)
                                currentScreen = AppScreen.CHECKOUT
                            }"""

text = text.replace(old_code, new_code)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)

