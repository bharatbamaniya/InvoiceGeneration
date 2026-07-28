import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    content = f.read()

# Update Top Bar
old_top_bar = """                title = {
                    Column {
                        Text(
                            text = state.storeName,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Quick Mobile Billing",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                actions = {
                    IconButton(
                        onClick = onManageItems,
                        modifier = Modifier.testTag("manage_items_button")
                    ) {
                        Icon(imageVector = Icons.Default.Inventory, contentDescription = "Manage Items")
                    }
                    IconButton(
                        onClick = onOpenHistory,
                        modifier = Modifier.testTag("history_button")
                    ) {
                        Icon(imageVector = Icons.Default.History, contentDescription = "History")
                    }
                    IconButton(
                        onClick = { showStoreSettingsDialog = true },
                        modifier = Modifier.testTag("store_settings_button")
                    ) {
                        Icon(imageVector = Icons.Default.Settings, contentDescription = "Store Settings")
                    }
                },"""
new_top_bar = """                title = {
                    val customerName = if (state.selectedCustomerId != null) {
                        state.customers.find { it.id == state.selectedCustomerId }?.name ?: "Unknown Customer"
                    } else {
                        "Unknown Customer"
                    }
                    Column {
                        Text(
                            text = customerName,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "New Invoice",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                actions = {
                    IconButton(
                        onClick = onManageItems,
                        modifier = Modifier.testTag("manage_items_button")
                    ) {
                        Icon(imageVector = Icons.Default.Inventory, contentDescription = "Manage Items")
                    }
                },"""
content = content.replace(old_top_bar, new_top_bar)

# Remove Customer Details section entirely
# Since it uses regex or just string splitting, let's use string split:
start_str = "            // Customer Details Input Section"
end_str = "            // Search Bar & Add Custom Item Action"

if start_str in content and end_str in content:
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    content = content[:start_idx] + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(content)
