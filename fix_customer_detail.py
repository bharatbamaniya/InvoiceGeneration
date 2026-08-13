import re

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'r') as f:
    text = f.read()

# Add parameter
text = text.replace("    onSettleBalance: (Customer, Double) -> Unit", "    onSettleBalance: (Customer, Double) -> Unit,\n    onEditInvoice: (Invoice) -> Unit")
text = text.replace("import androidx.compose.material.icons.filled.Receipt", "import androidx.compose.material.icons.filled.Receipt\nimport androidx.compose.material.icons.filled.Edit")

# Add edit icon button to the invoice card
old_invoice_row = """                                Text(
                                    "+ $currencySymbol${String.format(Locale.US, "%.2f", item.billAmount)}",
                                    color = MaterialTheme.colorScheme.error,
                                    fontWeight = FontWeight.Bold
                                )"""

new_invoice_row = """                                Column(horizontalAlignment = Alignment.End) {
                                    Text(
                                        "+ $currencySymbol${String.format(Locale.US, "%.2f", item.billAmount)}",
                                        color = MaterialTheme.colorScheme.error,
                                        fontWeight = FontWeight.Bold
                                    )
                                    IconButton(onClick = { onEditInvoice(item) }, modifier = Modifier.size(32.dp)) {
                                        Icon(Icons.Default.Edit, contentDescription = "Edit Invoice", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                                    }
                                }"""

text = text.replace(old_invoice_row, new_invoice_row)

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'w') as f:
    f.write(text)

