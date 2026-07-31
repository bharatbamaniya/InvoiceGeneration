import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),", "keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),\n                            readOnly = true,")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

