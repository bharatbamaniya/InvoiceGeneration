import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

pattern = r"Text\(cartItem\.item\.name, fontWeight = FontWeight\.Bold, modifier = Modifier\.weight\(1f\), maxLines = 1\).*?IconButton\(onClick = \{ onRemoveItem\(cartItem\.item\.id\) \}, modifier = Modifier\.size\(24\.dp\)\) \{\s*Icon\(Icons\.Default\.Delete, contentDescription = \"Remove\", tint = MaterialTheme\.colorScheme\.error\)\s*\}"

new_row = """Column(modifier = Modifier.weight(1f)) {
                                Text(cartItem.item.name, fontWeight = FontWeight.Bold, maxLines = 1)
                                val qtyFormat = if (cartItem.quantity % 1.0 == 0.0) cartItem.quantity.toInt().toString() else cartItem.quantity.toString()
                                val price = cartItem.customPrice ?: cartItem.item.price
                                val priceFormat = if (price % 1.0 == 0.0) price.toInt().toString() else price.toString()
                                Text("$qtyFormat ${cartItem.item.unit} x ${state.customer?.currencySymbol ?: "$"}$priceFormat", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            
                            val itemTotal = cartItem.quantity * (cartItem.customPrice ?: cartItem.item.price)
                            val totalFormat = if (itemTotal % 1.0 == 0.0) itemTotal.toInt().toString() else String.format(java.util.Locale.US, "%.2f", itemTotal)
                            Text("${state.customer?.currencySymbol ?: "$"}$totalFormat", fontWeight = FontWeight.Bold)
                            
                            Spacer(modifier = Modifier.width(16.dp))
                            
                            IconButton(onClick = { onRemoveItem(cartItem.item.id) }, modifier = Modifier.size(24.dp)) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove", tint = MaterialTheme.colorScheme.error)
                            }"""

text = re.sub(pattern, new_row, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
