with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

# Add onManageItems parameter
text = text.replace("onViewInvoices: () -> Unit", "onViewInvoices: () -> Unit,\n    onManageItems: () -> Unit")

# Replace first onViewInvoices with onManageItems
text = text.replace("IconButton(onClick = onViewInvoices) {\n                        Icon(Icons.Default.Inventory2, contentDescription = \"Archive\")\n                    }", "IconButton(onClick = onManageItems) {\n                        Icon(Icons.Default.Inventory2, contentDescription = \"Manage Items\")\n                    }")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

