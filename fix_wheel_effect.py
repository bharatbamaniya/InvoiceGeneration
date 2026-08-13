import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("LaunchedEffect(Unit) {\n        listState.scrollToItem(initialIndex)\n    }", "LaunchedEffect(initialIndex, range) {\n        listState.scrollToItem(initialIndex)\n    }")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

