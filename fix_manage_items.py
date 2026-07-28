import re

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    content = f.read()

# Add imports if needed
if 'import androidx.compose.material3.ExposedDropdownMenuBox' not in content:
    content = content.replace('import androidx.compose.material3.Text', 'import androidx.compose.material3.ExposedDropdownMenuBox\nimport androidx.compose.material3.DropdownMenuItem\nimport androidx.compose.material3.ExposedDropdownMenuDefaults\nimport androidx.compose.material3.Text')

# Remove category from onAddItem
content = re.sub(r'onAddItem: \(name: String, price: Double, category: String, unit: String\) -> Unit', 'onAddItem: (name: String, price: Double, unit: String) -> Unit', content)

# Remove text displaying category
content = re.sub(r'                            Text\(\s*text = item\.category,\s*style = MaterialTheme\.typography\.labelSmall,\s*color = MaterialTheme\.colorScheme\.primary\s*\)\s*', '', content)

# Modify dialog state variables
content = re.sub(r'        var category by remember \{ mutableStateOf\(editingItem\?\.category \?\: "Root"\) \}\n', '', content)

# Replace the unit textfield and remove category textfield
old_row = """                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = priceStr,
                            onValueChange = { priceStr = it; isError = false },
                            label = { Text("Price ($currencySymbol)") },
                            singleLine = true,
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                            modifier = Modifier.weight(1f)
                        )
                        OutlinedTextField(
                            value = unit,
                            onValueChange = { unit = it },
                            label = { Text("Unit") },
                            singleLine = true,
                            modifier = Modifier.weight(1f)
                        )
                    }
                    OutlinedTextField(
                        value = category,
                        onValueChange = { category = it },
                        label = { Text("Category") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth()
                    )"""

new_row = """                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = priceStr,
                            onValueChange = { priceStr = it; isError = false },
                            label = { Text("Price ($currencySymbol)") },
                            singleLine = true,
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                            modifier = Modifier.weight(1f)
                        )
                        var expanded by remember { mutableStateOf(false) }
                        val unitOptions = listOf("kg", "pc", "bunch", "gm")
                        ExposedDropdownMenuBox(
                            expanded = expanded,
                            onExpandedChange = { expanded = !expanded },
                            modifier = Modifier.weight(1f)
                        ) {
                            OutlinedTextField(
                                value = unit,
                                onValueChange = {},
                                readOnly = true,
                                label = { Text("Unit") },
                                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                                modifier = Modifier.menuAnchor()
                            )
                            ExposedDropdownMenu(
                                expanded = expanded,
                                onDismissRequest = { expanded = false }
                            ) {
                                unitOptions.forEach { option ->
                                    DropdownMenuItem(
                                        text = { Text(option) },
                                        onClick = {
                                            unit = option
                                            expanded = false
                                        }
                                    )
                                }
                            }
                        }
                    }"""

content = content.replace(old_row, new_row)

# Update the callbacks
content = re.sub(r'onUpdateItem\(editingItem!!\.copy\(name = name, price = price, category = category, unit = unit\)\)', 'onUpdateItem(editingItem!!.copy(name = name, price = price, unit = unit))', content)
content = re.sub(r'onAddItem\(name, price, category, unit\)', 'onAddItem(name, price, unit)', content)

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(content)

