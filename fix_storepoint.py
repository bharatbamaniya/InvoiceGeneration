import re

with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'r') as f:
    text = f.read()

bad_storepoint = """                        Column {
                            Text("StorePoint", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.height(16.dp))
                            Text("Customers", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                            Text("Manage outstanding balances", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }"""

good_storepoint = """                        Column {
                            Text("Customers", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                            Text("Manage outstanding balances", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }"""

text = text.replace(bad_storepoint, good_storepoint)

with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'w') as f:
    f.write(text)

