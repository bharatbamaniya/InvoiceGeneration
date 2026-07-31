import re

# 1. Fix CheckoutScreen.kt
with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    checkout = f.read()

# Add onUpdatePreviousOutstanding to CheckoutSummarySheet signature
checkout = checkout.replace(
    "onUpdatePrice: (String, Double) -> Unit,\n    onUpdateCash: (Double) -> Unit",
    "onUpdatePrice: (String, Double) -> Unit,\n    onUpdateCash: (Double) -> Unit,\n    onUpdatePreviousOutstanding: (Double) -> Unit"
)

# Update the call to CheckoutSummarySheet in CheckoutScreen
checkout = checkout.replace(
    "onUpdateCash = onUpdateCashReceived\n            )",
    "onUpdateCash = onUpdateCashReceived,\n                onUpdatePreviousOutstanding = onUpdatePreviousOutstanding\n            )"
)

# Fix the mock inside CheckoutSummarySheet
checkout = checkout.replace(
    "onValueChange = { /* handled by parent but mocked here for UI */ },",
    "onValueChange = { \n                        onUpdatePreviousOutstanding(it.toDoubleOrNull() ?: 0.0) \n                    },"
)

# Fix the mock slider in ItemConfigDialog
old_slider_mock = """                // Quantity Picker mock
                Text("150", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), fontSize = 14.sp)
                Spacer(modifier = Modifier.height(4.dp))
                Surface(
                    color = MaterialTheme.colorScheme.surfaceVariant,
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.fillMaxWidth().height(48.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        OutlinedTextField(
                            value = qtyStr,
                            onValueChange = { qtyStr = it },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            textStyle = LocalTextStyle.current.copy(textAlign = TextAlign.Center, fontWeight = FontWeight.Bold, fontSize = 20.sp),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Color.Transparent,
                                unfocusedBorderColor = Color.Transparent,
                                focusedContainerColor = Color.Transparent,
                                unfocusedContainerColor = Color.Transparent
                            ),
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                }
                Spacer(modifier = Modifier.height(4.dp))
                Text("250", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), fontSize = 14.sp)"""

new_slider = """                // Real Quantity Picker
                var sliderValue by remember { mutableStateOf((qtyStr.toFloatOrNull() ?: 1f).coerceIn(0f, 100f)) }
                
                Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("0", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), fontSize = 14.sp)
                    Slider(
                        value = sliderValue,
                        onValueChange = { 
                            sliderValue = it
                            qtyStr = String.format(Locale.US, "%.1f", it)
                        },
                        valueRange = 0f..100f,
                        modifier = Modifier.weight(1f).padding(horizontal = 8.dp)
                    )
                    Text("100", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), fontSize = 14.sp)
                }
                
                Surface(
                    color = MaterialTheme.colorScheme.surfaceVariant,
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.fillMaxWidth().height(48.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        OutlinedTextField(
                            value = qtyStr,
                            onValueChange = { 
                                qtyStr = it 
                                sliderValue = (it.toFloatOrNull() ?: 0f).coerceIn(0f, 100f)
                            },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            textStyle = LocalTextStyle.current.copy(textAlign = TextAlign.Center, fontWeight = FontWeight.Bold, fontSize = 20.sp),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Color.Transparent,
                                unfocusedBorderColor = Color.Transparent,
                                focusedContainerColor = Color.Transparent,
                                unfocusedContainerColor = Color.Transparent
                            ),
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                }"""

checkout = checkout.replace(old_slider_mock, new_slider)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(checkout)

# 2. Fix InvoiceDetailScreen.kt
with open('app/src/main/java/com/example/ui/screens/InvoiceDetailScreen.kt', 'r') as f:
    invoice_detail = f.read()

old_toast = """Toast.makeText(context, "PDF Export and Sharing coming soon", Toast.LENGTH_SHORT).show()"""
new_share = """val shareIntent = android.content.Intent(android.content.Intent.ACTION_SEND).apply {
                                type = "text/plain"
                                putExtra(android.content.Intent.EXTRA_TEXT, "Invoice ${invoice.invoiceId} for ${invoice.customerName}\\nAmount: ${invoice.billAmount}\\nStatus: ${if(invoice.totalBalance <= 0.0) "PAID" else "UNPAID"}")
                            }
                            context.startActivity(android.content.Intent.createChooser(shareIntent, "Share Invoice"))"""

invoice_detail = invoice_detail.replace(old_toast, new_share)

with open('app/src/main/java/com/example/ui/screens/InvoiceDetailScreen.kt', 'w') as f:
    f.write(invoice_detail)

# 3. Fix InvoiceHistoryScreen.kt
with open('app/src/main/java/com/example/ui/screens/InvoiceHistoryScreen.kt', 'r') as f:
    invoice_history = f.read()

invoice_history = invoice_history.replace(
    "fun InvoiceHistoryScreen(",
    "import androidx.compose.runtime.*\nfun InvoiceHistoryScreen("
)
invoice_history = invoice_history.replace(
    ") {\n    Scaffold(",
    ") {\n    var searchQuery by remember { mutableStateOf(\"\") }\n    var isSearchActive by remember { mutableStateOf(false) }\n    val filteredInvoices = if (searchQuery.isEmpty()) invoices else invoices.filter { it.customerName.contains(searchQuery, ignoreCase = true) || it.invoiceId.toString().contains(searchQuery) }\n    Scaffold("
)
invoice_history = invoice_history.replace(
    "title = { Text(\"Invoice History\", fontWeight = FontWeight.Bold) },",
    """title = { 
                    if (isSearchActive) {
                        OutlinedTextField(
                            value = searchQuery,
                            onValueChange = { searchQuery = it },
                            placeholder = { Text("Search invoices...") },
                            singleLine = true,
                            modifier = Modifier.fillMaxWidth().height(50.dp)
                        )
                    } else {
                        Text("Invoice History", fontWeight = FontWeight.Bold) 
                    }
                },"""
)
invoice_history = invoice_history.replace(
    "IconButton(onClick = { /* Search */ }) {",
    "IconButton(onClick = { isSearchActive = !isSearchActive; if (!isSearchActive) searchQuery = \"\" }) {"
)
invoice_history = invoice_history.replace(
    "if (invoices.isEmpty()) {",
    "if (filteredInvoices.isEmpty()) {"
)
invoice_history = invoice_history.replace(
    "items(invoices.sortedByDescending { it.dateMillis }) { invoice ->",
    "items(filteredInvoices.sortedByDescending { it.dateMillis }) { invoice ->"
)

with open('app/src/main/java/com/example/ui/screens/InvoiceHistoryScreen.kt', 'w') as f:
    f.write(invoice_history)

