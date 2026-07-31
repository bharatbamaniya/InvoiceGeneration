import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Add imports
imports = """import androidx.compose.ui.res.stringResource
import com.example.R
"""
text = text.replace("import com.example.viewmodel.InvoiceUiState", "import com.example.viewmodel.InvoiceUiState\n" + imports)

# Remove Actions Group
actions_group = """            item {
                Spacer(modifier = Modifier.height(16.dp))
                SectionHeader("Actions Group")
                
                ListItem(
                    headlineContent = { Text("Enable Swipe to Delete", fontWeight = FontWeight.Bold) },
                    supportingContent = { Text("Allow swiping items to remove them from lists.", color = MaterialTheme.colorScheme.onSurfaceVariant) },
                    trailingContent = { 
                        Switch(
                            checked = swipeToDeleteEnabled, 
                            onCheckedChange = { 
                                swipeToDeleteEnabled = it
                                onUpdateStoreSettings(storeName, storeAddress, storePhone, ownerName, it)
                            }
                        ) 
                    },
                    colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.background)
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
            }"""

if actions_group in text:
    text = text.replace(actions_group, "")

# Fix app name
text = text.replace('Text("Material Ledger", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)', 'Text(stringResource(R.string.app_name), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)')

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

