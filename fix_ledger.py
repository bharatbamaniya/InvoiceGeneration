with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'r') as f:
    text = f.read()

# Add Payment import
if "import com.example.model.Payment" not in text:
    text = text.replace("import com.example.model.Invoice", "import com.example.model.Invoice\nimport com.example.model.Payment")

# Add payments parameter
text = text.replace("invoices: List<Invoice>,", "invoices: List<Invoice>,\n    payments: List<Payment>,")

# Find ledger rendering and replace
ledger_marker_start = "// Transactions list"
ledger_marker_end = "showSettleDialog = false"
# Actually, it's easier to regex out the transactions list part
# I will just write a python script to rewrite the Transactions list block
import re

# We need to combine invoices and payments by date
replacement = """// Transactions list
            val ledgerItems = mutableListOf<Pair<Long, Any>>() // Pair of timestamp and either Invoice or Payment
            invoices.filter { it.customerId == customer.id }.forEach { ledgerItems.add(Pair(it.dateMillis, it)) }
            payments.forEach { ledgerItems.add(Pair(it.dateMillis, it)) }
            val sortedLedger = ledgerItems.sortedByDescending { it.first }

            if (sortedLedger.isEmpty()) {
                item {
                    Text("No transactions found", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(16.dp))
                }
            } else {
                items(sortedLedger) { pair ->
                    val item = pair.second
                    val dateFormat = SimpleDateFormat("dd MMM yyyy, hh:mm a", Locale.getDefault())
                    val dateString = dateFormat.format(Date(pair.first))
                    
                    if (item is Invoice) {
                        // Show "Amount Received" if there was cash received during invoice creation
                        if (item.cashReceived > 0) {
                            Card(
                                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Row(
                                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Surface(
                                        shape = RoundedCornerShape(percent = 50),
                                        color = MaterialTheme.colorScheme.surfaceVariant,
                                        modifier = Modifier.size(40.dp)
                                    ) {
                                        Box(contentAlignment = Alignment.Center) {
                                            Icon(Icons.Default.Payment, contentDescription = null, modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                                        }
                                    }
                                    
                                    Spacer(modifier = Modifier.width(16.dp))
                                    
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text("Payment Received", fontWeight = FontWeight.Bold)
                                        Text(dateString, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    }
                                    
                                    Text(
                                        "- $currencySymbol${String.format(Locale.US, "%.2f", item.cashReceived)}",
                                        color = MaterialTheme.colorScheme.primary,
                                        fontWeight = FontWeight.Bold
                                    )
                                }
                            }
                        }
                        
                        // Invoice Card
                        Card(
                            modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                            shape = RoundedCornerShape(12.dp),
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Surface(
                                    shape = RoundedCornerShape(percent = 50),
                                    color = MaterialTheme.colorScheme.primaryContainer,
                                    modifier = Modifier.size(40.dp)
                                ) {
                                    Box(contentAlignment = Alignment.Center) {
                                        Icon(Icons.Default.Receipt, contentDescription = null, modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.onPrimaryContainer)
                                    }
                                }
                                
                                Spacer(modifier = Modifier.width(16.dp))
                                
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(item.invoiceId, fontWeight = FontWeight.Bold)
                                    Text(dateString, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                }
                                
                                Text(
                                    "+ $currencySymbol${String.format(Locale.US, "%.2f", item.billAmount)}",
                                    color = MaterialTheme.colorScheme.error,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    } else if (item is Payment) {
                        Card(
                            modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)),
                            shape = RoundedCornerShape(12.dp)
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Surface(
                                    shape = RoundedCornerShape(percent = 50),
                                    color = MaterialTheme.colorScheme.surfaceVariant,
                                    modifier = Modifier.size(40.dp)
                                ) {
                                    Box(contentAlignment = Alignment.Center) {
                                        Icon(Icons.Default.Payment, contentDescription = null, modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                                    }
                                }
                                
                                Spacer(modifier = Modifier.width(16.dp))
                                
                                Column(modifier = Modifier.weight(1f)) {
                                    Text("Payment Received", fontWeight = FontWeight.Bold)
                                    Text(dateString, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    if (item.remark.isNotBlank()) {
                                        Text(item.remark, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    }
                                }
                                
                                Text(
                                    "- $currencySymbol${String.format(Locale.US, "%.2f", item.amount)}",
                                    color = MaterialTheme.colorScheme.primary,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                }
            }"""

# Use regex to replace the old Transactions list
start = text.find("// Transactions list")
if start != -1:
    end = text.find("if (showSettleDialog)")
    if end != -1:
        text = text[:start] + replacement + "\n\n            " + text[end:]

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'w') as f:
    f.write(text)

with open('app/src/main/java/com/example/ui/screens/InvoiceDetailScreen.kt', 'r') as f:
    text2 = f.read()

# Remove computer generated note
start_text = """Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            "This is a computer-generated invoice, does not require a physical signature",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            textAlign = TextAlign.Center
                        )"""
text2 = text2.replace(start_text, "")
with open('app/src/main/java/com/example/ui/screens/InvoiceDetailScreen.kt', 'w') as f:
    f.write(text2)

