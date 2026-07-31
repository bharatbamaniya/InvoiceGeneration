import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

pattern = r"// Unit toggle.*?if \(item\.unit == \"kg\"\) \{.*?Row\(.*?\).*?Surface\(.*?modifier = Modifier\.clickable \{.*?isGm = false.*?val qty = qtyStr.*?if \(qty > 10\).*?\}.*?\{.*?Text\(\"kg\".*?\).*?Surface\(.*?modifier = Modifier\.clickable \{.*?isGm = true.*?val qty = qtyStr.*?if \(qty < 10\).*?\}.*?\{.*?Text\(\"gm\".*?\).*?\}.*?\}.*?\}"

new_unit_toggle = """                // Unit toggle
                if (item.unit == "kg") {
                    Row(
                        modifier = Modifier.padding(bottom = 24.dp).background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(24.dp))
                    ) {
                        Surface(
                            color = if (!isGm) MaterialTheme.colorScheme.primary else Color.Transparent,
                            shape = RoundedCornerShape(24.dp),
                            modifier = Modifier.clickable { 
                                isGm = false
                            }
                        ) {
                            Text("kg", modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp), color = if (!isGm) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                        Surface(
                            color = if (isGm) MaterialTheme.colorScheme.primary else Color.Transparent,
                            shape = RoundedCornerShape(24.dp),
                            modifier = Modifier.clickable { 
                                isGm = true
                            }
                        ) {
                            Text("gm", modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp), color = if (isGm) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                    }
                }"""

text = re.sub(pattern, new_unit_toggle, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

