import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

pattern = r"Text\(\s*text = qtyStr,\s*style = MaterialTheme\.typography\.displayMedium,\s*fontWeight = FontWeight\.Bold,\s*color = MaterialTheme\.colorScheme\.onSurface,\s*modifier = Modifier\.padding\(vertical = 16\.dp\)\s*\)"

new_text = """Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 16.dp)) {
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
                }"""

text = re.sub(pattern, new_text, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

