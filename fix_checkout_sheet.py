import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

old_block = """fun CheckoutSummarySheet(
    state: InvoiceUiState,
    onDismiss: () -> Unit,
    onGenerateInvoice: () -> Unit,
    onClearCart: () -> Unit,
    onRemoveItem: (String) -> Unit,
    onUpdateQty: (String, Double) -> Unit,
    onUpdatePrice: (String, Double) -> Unit,
    onUpdateCash: (Double) -> Unit,
    onUpdatePreviousOutstanding: (Double) -> Unit
) {
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = MaterialTheme.colorScheme.background,
        dragHandle = { BottomSheetDefaults.DragHandle() }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 8.dp)
                .padding(bottom = 32.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Checkout Summary", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                TextButton(onClick = onClearCart) {
                    Icon(Icons.Default.Delete, contentDescription = "Clear All", modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("Clear All")
                }
            }
            
            Text("${state.cartItems.size} items selected", color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(bottom = 16.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("View/Edit Items (${state.cartItems.size})", fontWeight = FontWeight.Bold)
                Icon(Icons.Default.KeyboardArrowUp, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Items List
            Column(
                modifier = Modifier.heightIn(max = 200.dp).fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                state.cartItems.forEach { cartItem ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Surface(
                            shape = RoundedCornerShape(percent = 50),
                            color = MaterialTheme.colorScheme.surfaceVariant,
                            modifier = Modifier.size(32.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Text(cartItem.item.name.take(1).uppercase(), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                        
                        Spacer(modifier = Modifier.width(8.dp))
                        
                        Text(cartItem.item.name, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                        
                        // Qty input
                        OutlinedTextField(
                            value = cartItem.quantity.toString(),
                            onValueChange = { onUpdateQty(cartItem.item.id, it.toDoubleOrNull() ?: 0.0) },
                            modifier = Modifier.width(60.dp).height(48.dp),
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            label = { Text("Qty", fontSize = 10.sp) },
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                                unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                            )
                        )
                        
                        Spacer(modifier = Modifier.width(8.dp))
                        
                        // Price input
                        OutlinedTextField(
                            value = cartItem.customPrice?.toString() ?: cartItem.item.price.toString(),
                            onValueChange = { onUpdatePrice(cartItem.item.id, it.toDoubleOrNull() ?: 0.0) },
                            modifier = Modifier.width(80.dp).height(48.dp),
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            label = { Text(state.currencySymbol, fontSize = 10.sp) },
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                                unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                            )
                        )
                        
                        Spacer(modifier = Modifier.width(8.dp))
                        
                        IconButton(onClick = { onRemoveItem(cartItem.item.id) }, modifier = Modifier.size(24.dp)) {
                            Icon(Icons.Default.Delete, contentDescription = "Remove", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            HorizontalDivider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Bill Amount:", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("${state.currencySymbol}${String.format(Locale.US, "%.2f", state.cartItems.sumOf { it.totalPrice })}", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedTextField(
                    value = state.previousOutstanding.toString(),
                    onValueChange = { 
                        onUpdatePreviousOutstanding(it.toDoubleOrNull() ?: 0.0) 
                    },
                    label = { Text("Prev Outstanding", fontSize = 10.sp) },
                    modifier = Modifier.weight(1f),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                    )
                )
                
                var cashStr by remember { mutableStateOf("") }
                OutlinedTextField(
                    value = cashStr,
                    onValueChange = { 
                        cashStr = it
                        onUpdateCash(it.toDoubleOrNull() ?: 0.0) 
                    },
                    label = { Text("Cash Received", fontSize = 10.sp) },
                    modifier = Modifier.weight(1f),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                    )
                )
            }"""

new_block = """fun CheckoutSummarySheet(
    state: InvoiceUiState,
    onDismiss: () -> Unit,
    onGenerateInvoice: () -> Unit,
    onClearCart: () -> Unit,
    onRemoveItem: (String) -> Unit,
    onUpdateQty: (String, Double) -> Unit,
    onUpdatePrice: (String, Double) -> Unit,
    onUpdateCash: (Double) -> Unit,
    onUpdatePreviousOutstanding: (Double) -> Unit
) {
    var itemsExpanded by remember { mutableStateOf(false) }
    var billExpanded by remember { mutableStateOf(false) }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = MaterialTheme.colorScheme.background,
        dragHandle = { BottomSheetDefaults.DragHandle() }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 8.dp)
                .padding(bottom = 32.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Checkout Summary", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                TextButton(onClick = onClearCart) {
                    Icon(Icons.Default.Delete, contentDescription = "Clear All", modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("Clear All")
                }
            }
            
            Text("${state.cartItems.size} items selected", color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(bottom = 16.dp))
            
            Row(modifier = Modifier.fillMaxWidth().clickable { itemsExpanded = !itemsExpanded }.padding(vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("View/Edit Items (${state.cartItems.size})", fontWeight = FontWeight.Bold)
                Icon(if (itemsExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            
            if (itemsExpanded) {
                Spacer(modifier = Modifier.height(16.dp))
                
                // Items List
                Column(
                    modifier = Modifier.heightIn(max = 240.dp).fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    state.cartItems.forEach { cartItem ->
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Surface(
                                shape = RoundedCornerShape(percent = 50),
                                color = MaterialTheme.colorScheme.surfaceVariant,
                                modifier = Modifier.size(32.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Text(cartItem.item.name.take(1).uppercase(), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                }
                            }
                            
                            Spacer(modifier = Modifier.width(8.dp))
                            
                            Text(cartItem.item.name, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f), maxLines = 1)
                            
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
                            }
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            HorizontalDivider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth().clickable { billExpanded = !billExpanded }.padding(vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Bill Amount:", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.width(8.dp))
                    Icon(if (billExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                Text("${state.currencySymbol}${String.format(Locale.US, "%.2f", state.cartItems.sumOf { it.totalPrice })}", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            }
            
            if (billExpanded) {
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    OutlinedTextField(
                        value = state.previousOutstanding.toString(),
                        onValueChange = { 
                            onUpdatePreviousOutstanding(it.toDoubleOrNull() ?: 0.0) 
                        },
                        label = { Text("Prev Outstanding", fontSize = 10.sp) },
                        modifier = Modifier.weight(1f),
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                            unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        )
                    )
                    
                    var cashStr by remember { mutableStateOf("") }
                    OutlinedTextField(
                        value = cashStr,
                        onValueChange = { 
                            cashStr = it
                            onUpdateCash(it.toDoubleOrNull() ?: 0.0) 
                        },
                        label = { Text("Cash Received", fontSize = 10.sp) },
                        modifier = Modifier.weight(1f),
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                            unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        )
                    )
                }
            }"""

if old_block in text:
    print("Found block!")
else:
    print("Block not found!")

text = text.replace(old_block, new_block)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

