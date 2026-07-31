import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

pattern = r"(// Numpad for quantity.*?)(Surface\(\s*color = MaterialTheme\.colorScheme\.surfaceVariant,\s*shape = RoundedCornerShape\(12\.dp\),\s*modifier = Modifier\.fillMaxWidth\(\)\.height\(48\.dp\)\s*\)\s*\{\s*Box\(contentAlignment = Alignment\.Center\) \{\s*OutlinedTextField\(.*?\)\s*\}\s*\})"

# Swap them
def swap(match):
    return match.group(2) + "\n\n" + match.group(1)

new_text = re.sub(pattern, swap, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(new_text)

