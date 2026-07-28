import re

with open('app/src/main/java/com/example/ui/components/AddCustomItemDialog.kt', 'r') as f:
    content = f.read()

if 'import androidx.compose.material3.ExposedDropdownMenuBox' not in content:
    content = content.replace('import androidx.compose.material3.Text', 'import androidx.compose.material3.ExposedDropdownMenuBox\nimport androidx.compose.material3.DropdownMenuItem\nimport androidx.compose.material3.ExposedDropdownMenuDefaults\nimport androidx.compose.material3.ExperimentalMaterial3Api\nimport androidx.compose.material3.Text')

old_row = """                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = {
                            priceStr = it
                            isError = false
                        },
                        label = { Text("Price ($currencySymbol)") },
                        placeholder = { Text("0.00") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                        modifier = Modifier
                            .weight(1f)
                            .testTag("custom_item_price_input")
                    )
                    OutlinedTextField(
                        value = unit,
                        onValueChange = { unit = it },
                        label = { Text("Unit") },
                        placeholder = { Text("kg / pc / bottle") },
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )
                }"""

new_row = """                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = {
                            priceStr = it
                            isError = false
                        },
                        label = { Text("Price ($currencySymbol)") },
                        placeholder = { Text("0.00") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                        modifier = Modifier
                            .weight(1f)
                            .testTag("custom_item_price_input")
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
content = content.replace('@Composable\nfun AddCustomItemDialog', '@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun AddCustomItemDialog')

with open('app/src/main/java/com/example/ui/components/AddCustomItemDialog.kt', 'w') as f:
    f.write(content)

