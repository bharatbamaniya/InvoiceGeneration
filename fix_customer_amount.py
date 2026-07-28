import re

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'r') as f:
    content = f.read()

old_balance = """                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text("Outstanding Balance", style = MaterialTheme.typography.titleMedium)
                    Text(
                        "$currencySymbol${String.format("%.2f", customer.balance)}",
                        style = MaterialTheme.typography.headlineMedium,
                        fontWeight = FontWeight.Bold,
                        color = if (customer.balance > 0) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    
                    if (customer.balance > 0) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Button(onClick = { showSettleDialog = true }) {
                            Text("Settle Balance")
                        }
                    }
                }"""

new_balance = """                Row(
                    modifier = Modifier.padding(16.dp).fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("Outstanding Balance", style = MaterialTheme.typography.titleMedium)
                        if (customer.balance > 0) {
                            Button(onClick = { showSettleDialog = true }) {
                                Text("Settle Balance")
                            }
                        }
                    }
                    Text(
                        "$currencySymbol${String.format("%.2f", customer.balance)}",
                        style = MaterialTheme.typography.headlineMedium,
                        fontWeight = FontWeight.Bold,
                        color = if (customer.balance > 0) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }"""

content = content.replace(old_balance, new_balance)

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'w') as f:
    f.write(content)
