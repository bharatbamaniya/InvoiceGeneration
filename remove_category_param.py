import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    content = f.read()

content = re.sub(r'\s*onCategorySelect: \(String\) -> Unit,\n', '\n', content)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(content)
