import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    checkout = f.read()

# Add state
checkout = checkout.replace(
    "    var selectedItemForConfig by remember { mutableStateOf<GroceryItem?>(null) }",
    "    var selectedItemForConfig by remember { mutableStateOf<GroceryItem?>(null) }\n    var showCustomItemDialog by remember { mutableStateOf(false) }"
)

# Add custom item click listener to the Add Item button
checkout = checkout.replace(
    "onClick = onManageItems,",
    "onClick = { showCustomItemDialog = true },"
)

# Replace "TAP TO ADD TO INVOICE" with a button for manage items maybe? 
checkout = checkout.replace(
    'Text(\n                "TAP TO ADD TO INVOICE',
    """Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(
                    "TAP TO ADD TO INVOICE (${allAvailableItems.size})",
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                TextButton(onClick = onManageItems) {
                    Text("Manage Catalog")
                }
            }
            // Text(\n                "TAP TO ADD TO INVOICE"""
)

# Add the CustomItemDialog component at the end of CheckoutScreen
dialog_code = """
        if (showCustomItemDialog) {
            CustomItemDialog(
                currencySymbol = state.currencySymbol,
                onDismiss = { showCustomItemDialog = false },
                onConfirm = { name, price, unit ->
                    onAddCustomItem(name, price, unit)
                    showCustomItemDialog = false
                }
            )
        }
"""

checkout = checkout.replace(
    "        if (selectedItemForConfig != null) {",
    dialog_code + "        if (selectedItemForConfig != null) {"
)

custom_dialog_composable = """
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CustomItemDialog(
    currencySymbol: String,
    onDismiss: () -> Unit,
    onConfirm: (String, Double, String) -> Unit
) {
    var name by remember { mutableStateOf("") }
    var priceStr by remember { mutableStateOf("") }
    var unit by remember { mutableStateOf("kg") }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add Custom Item") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Item Name") },
                    modifier = Modifier.fillMaxWidth()
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = { priceStr = it },
                        label = { Text("Price ($currencySymbol)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f)
                    )
                    OutlinedTextField(
                        value = unit,
                        onValueChange = { unit = it },
                        label = { Text("Unit") },
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val price = priceStr.toDoubleOrNull() ?: 0.0
                    if (name.isNotBlank() && price > 0) {
                        onConfirm(name, price, unit)
                    }
                }
            ) {
                Text("Add")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
"""

checkout += custom_dialog_composable

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(checkout)

