import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("state.cartItems.sumOf { it.customPrice * it.quantity }", "state.cartItems.sumOf { (it.customPrice ?: it.item.price) * it.quantity }")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(content)

