import re

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'r') as f:
    content = f.read()

imports = """import com.example.model.Customer
import com.example.model.Invoice
import com.example.model.Payment
import androidx.compose.ui.graphics.Color"""

content = content.replace("import com.example.model.Customer\nimport com.example.model.Invoice", imports)

sig_old = """fun CustomerDetailScreen(
    customer: Customer,
    invoices: List<Invoice>,
    currencySymbol: String,"""

sig_new = """fun CustomerDetailScreen(
    customer: Customer,
    invoices: List<Invoice>,
    payments: List<Payment>,
    currencySymbol: String,"""

content = content.replace(sig_old, sig_new)

ledger_logic = """
    val dateFormat = remember { SimpleDateFormat("dd MMM yyyy, hh:mm a", Locale.getDefault()) }
    
    val ledger = remember(invoices, payments) {
        val ledgerInvoices = invoices.map { LedgerItem.InvoiceItem(it) }
        val ledgerPayments = payments.map { LedgerItem.PaymentItem(it) }
        (ledgerInvoices + ledgerPayments).sortedByDescending { it.dateMillis }
    }
"""

content = content.replace("    val dateFormat = remember { SimpleDateFormat(\"dd MMM yyyy, hh:mm a\", Locale.getDefault()) }", ledger_logic)

history_old = """            Text("Invoice History", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(8.dp))
            
            if (invoices.isEmpty()) {
                Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                    Text("No invoices yet.")
                }
            } else {
                LazyColumn(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(invoices) { invoice ->
                        Card(
                            modifier = Modifier.fillMaxWidth().clickable { onViewInvoice(invoice) },
                        ) {
                            Row(
                                modifier = Modifier.padding(16.dp).fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column {
                                    Text(invoice.invoiceId, fontWeight = FontWeight.Bold)
                                    Text(dateFormat.format(Date(invoice.dateMillis)), style = MaterialTheme.typography.bodySmall)
                                }
                                Text("$currencySymbol${String.format("%.2f", invoice.billAmount)}", fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }"""

history_new = """            Text("Transaction Ledger", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(8.dp))
            
            if (ledger.isEmpty()) {
                Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                    Text("No transactions yet.")
                }
            } else {
                LazyColumn(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(ledger) { entry ->
                        when(entry) {
                            is LedgerItem.InvoiceItem -> {
                                Card(
                                    modifier = Modifier.fillMaxWidth().clickable { onViewInvoice(entry.invoice) },
                                ) {
                                    Row(
                                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Column {
                                            Text(entry.invoice.invoiceId, fontWeight = FontWeight.Bold)
                                            Text(dateFormat.format(Date(entry.dateMillis)), style = MaterialTheme.typography.bodySmall)
                                        }
                                        Text("+ $currencySymbol${String.format("%.2f", entry.invoice.billAmount)}", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.error)
                                    }
                                }
                            }
                            is LedgerItem.PaymentItem -> {
                                Card(
                                    modifier = Modifier.fillMaxWidth(),
                                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.tertiaryContainer)
                                ) {
                                    Row(
                                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Column {
                                            Text("Payment Received", fontWeight = FontWeight.Bold)
                                            Text(dateFormat.format(Date(entry.dateMillis)), style = MaterialTheme.typography.bodySmall)
                                        }
                                        Text("- $currencySymbol${String.format("%.2f", entry.payment.amount)}", fontWeight = FontWeight.Bold, color = Color(0xFF2E7D32)) // Dark green
                                    }
                                }
                            }
                        }
                    }
                }
            }"""

content = content.replace(history_old, history_new)

sealed_class = """
sealed class LedgerItem {
    abstract val dateMillis: Long
    data class InvoiceItem(val invoice: Invoice) : LedgerItem() {
        override val dateMillis = invoice.dateMillis
    }
    data class PaymentItem(val payment: Payment) : LedgerItem() {
        override val dateMillis = payment.dateMillis
    }
}
"""

content = content + sealed_class

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'w') as f:
    f.write(content)
