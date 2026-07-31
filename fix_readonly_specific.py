import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

pattern = r"(OutlinedTextField\(\s*value = qtyStr,\s*onValueChange = \{\s*qtyStr = it\s*\},\s*keyboardOptions = KeyboardOptions\(keyboardType = KeyboardType\.Number\),)"

def replace(match):
    return match.group(1) + "\n                            readOnly = true,"

new_text = re.sub(pattern, replace, text, count=1)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(new_text)

