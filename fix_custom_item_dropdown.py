import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

old_custom_item = """fun CustomItemDialog(
    currencySymbol: String,
    onDismiss: () -> Unit,
    onConfirm: (String, Double, String) -> Unit
) {
    var name by remember { mutableStateOf("") }
    var priceStr by remember { mutableStateOf("") }
    var unit by remember { mutableStateOf("kg") }

    AlertDialog("""

new_custom_item = """fun CustomItemDialog(
    currencySymbol: String,
    onDismiss: () -> Unit,
    onConfirm: (String, Double, String) -> Unit
) {
    var name by remember { mutableStateOf("") }
    var priceStr by remember { mutableStateOf("") }
    var unit by remember { mutableStateOf("kg") }
    val units = listOf("kg", "gm", "pc", "bunch")
    var expanded by remember { mutableStateOf(false) }

    AlertDialog("""

text = text.replace(old_custom_item, new_custom_item)

old_unit_field = """                    OutlinedTextField(
                        value = unit,
                        onValueChange = { unit = it },
                        label = { Text("Unit") },
                        modifier = Modifier.weight(1f)
                    )"""

new_unit_field = """                    ExposedDropdownMenuBox(
                        expanded = expanded,
                        onExpandedChange = { expanded = !expanded },
                        modifier = Modifier.weight(1f)
                    ) {
                        OutlinedTextField(
                            value = unit,
                            onValueChange = {},
                            readOnly = true,
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                            modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth(),
                            label = { Text("Unit") }
                        )
                        ExposedDropdownMenu(
                            expanded = expanded,
                            onDismissRequest = { expanded = false },
                            modifier = Modifier
                        ) {
                            units.forEach { option ->
                                DropdownMenuItem(
                                    text = { Text(option) },
                                    onClick = {
                                        unit = option
                                        expanded = false
                                    }
                                )
                            }
                        }
                    }"""

text = text.replace(old_unit_field, new_unit_field)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

