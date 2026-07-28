import re

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'onSettleBalance: (amount: Double) -> Unit,',
    'onSettleBalance: (amount: Double, remark: String) -> Unit,'
)

content = content.replace(
    'var settleAmount by remember { mutableStateOf("") }',
    'var settleAmount by remember { mutableStateOf("") }\n    var settleRemark by remember { mutableStateOf("") }'
)

dialog_old = """                text = {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("Enter the amount received from ${customer.name}.")
                        OutlinedTextField(
                            value = settleAmount,
                            onValueChange = { settleAmount = it },
                            label = { Text("Amount ($currencySymbol)") },
                            singleLine = true
                        )
                    }
                },"""

dialog_new = """                text = {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("Enter the amount received from ${customer.name}.")
                        OutlinedTextField(
                            value = settleAmount,
                            onValueChange = { settleAmount = it },
                            label = { Text("Amount ($currencySymbol)") },
                            singleLine = true
                        )
                        OutlinedTextField(
                            value = settleRemark,
                            onValueChange = { settleRemark = it },
                            label = { Text("Remark (Optional)") },
                            singleLine = true
                        )
                    }
                },"""

content = content.replace(dialog_old, dialog_new)

confirm_old = """                    Button(onClick = {
                        val amount = settleAmount.toDoubleOrNull()
                        if (amount != null && amount > 0) {
                            onSettleBalance(amount)
                            showSettleDialog = false
                            settleAmount = ""
                        }
                    })"""

confirm_new = """                    Button(onClick = {
                        val amount = settleAmount.toDoubleOrNull()
                        if (amount != null && amount > 0) {
                            onSettleBalance(amount, settleRemark)
                            showSettleDialog = false
                            settleAmount = ""
                            settleRemark = ""
                        }
                    })"""

content = content.replace(confirm_old, confirm_new)

display_old = """                                            Text("Payment Received", fontWeight = FontWeight.Bold)
                                            Text(dateFormat.format(Date(entry.dateMillis)), style = MaterialTheme.typography.bodySmall)"""

display_new = """                                            Text("Payment Received", fontWeight = FontWeight.Bold)
                                            Text(dateFormat.format(Date(entry.dateMillis)), style = MaterialTheme.typography.bodySmall)
                                            if (entry.payment.remark.isNotBlank()) {
                                                Text("Remark: ${entry.payment.remark}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onTertiaryContainer.copy(alpha = 0.7f))
                                            }"""

content = content.replace(display_old, display_new)

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'w') as f:
    f.write(content)
