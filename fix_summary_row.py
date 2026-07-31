import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

old_row = """                            Text(cartItem.item.name, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f), maxLines = 1)
                               
                            Spacer(modifier = Modifier.width(8.dp))
                               
                            // Qty input
                            OutlinedTextField(
                                value = cartItem.quantity.toString(),
                                onValueChange = { onUpdateQty(cartItem.item.id, it.toDoubleOrNull() ?: 0.0) },
                                modifier = Modifier.weight(0.7f).height(48.dp),
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                                textStyle = LocalTextStyle.current.copy(fontSize = 12.sp),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                                    unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                                )
                            )
                               
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("x", fontSize = 12.sp)
                            Spacer(modifier = Modifier.width(4.dp))
                               
                            // Price input
                            OutlinedTextField(
                                value = cartItem.customPrice?.toString() ?: cartItem.item.price.toString(),
                                onValueChange = { onUpdatePrice(cartItem.item.id, it.toDoubleOrNull() ?: 0.0) },
                                modifier = Modifier.weight(0.7f).height(48.dp),
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                                textStyle = LocalTextStyle.current.copy(fontSize = 12.sp),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                                    unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                                )
                            )
                               
                            Spacer(modifier = Modifier.width(4.dp))
                               
                            IconButton(onClick = { onRemoveItem(cartItem.item.id) }, modifier = Modifier.size(24.dp)) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove", tint = MaterialTheme.colorScheme.error)
                            }"""

new_row = """                            Column(modifier = Modifier.weight(1f)) {
                                Text(cartItem.item.name, fontWeight = FontWeight.Bold, maxLines = 1)
                                val qtyFormat = if (cartItem.quantity % 1.0 == 0.0) cartItem.quantity.toInt().toString() else cartItem.quantity.toString()
                                val price = cartItem.customPrice ?: cartItem.item.price
                                val priceFormat = if (price % 1.0 == 0.0) price.toInt().toString() else price.toString()
                                Text("$qtyFormat ${cartItem.item.unit} x ${state.customer?.currencySymbol ?: "$"}$priceFormat", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            
                            val itemTotal = cartItem.quantity * (cartItem.customPrice ?: cartItem.item.price)
                            val totalFormat = if (itemTotal % 1.0 == 0.0) itemTotal.toInt().toString() else String.format(Locale.US, "%.2f", itemTotal)
                            Text("${state.customer?.currencySymbol ?: "$"}$totalFormat", fontWeight = FontWeight.Bold)
                            
                            Spacer(modifier = Modifier.width(16.dp))
                            
                            IconButton(onClick = { onRemoveItem(cartItem.item.id) }, modifier = Modifier.size(24.dp)) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove", tint = MaterialTheme.colorScheme.error)
                            }"""

if old_row in text:
    print("Found exact row match")
    text = text.replace(old_row, new_row)
else:
    print("Row not exact match, using regex")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
