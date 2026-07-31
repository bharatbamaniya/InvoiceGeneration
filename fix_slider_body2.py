import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

old = """val currentValue = qtyStr.toFloatOrNull() ?: 0f
                
                SimpleWheelPicker("""

new = """val currentValue = qtyStr.toFloatOrNull() ?: 0f
                
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 16.dp)) {
                    Text(
                        text = qtyStr,
                        style = MaterialTheme.typography.displayLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary,
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = if (isGm && item.unit == "kg") "gm" else item.unit,
                        style = MaterialTheme.typography.titleLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                SimpleWheelPicker("""

text = text.replace(old, new)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
