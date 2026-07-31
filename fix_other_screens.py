import re

# Update Settings Screen
with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    settings_code = f.read()

settings_code = settings_code.replace('TopAppBar(', 'CenterAlignedTopAppBar(')
settings_code = settings_code.replace('Button(', 'ElevatedButton(')

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(settings_code)

# Update Invoice History Screen
with open('app/src/main/java/com/example/ui/screens/InvoiceHistoryScreen.kt', 'r') as f:
    history_code = f.read()

history_code = history_code.replace('TopAppBar(', 'CenterAlignedTopAppBar(')
history_code = history_code.replace('Card(', 'ElevatedCard(')

with open('app/src/main/java/com/example/ui/screens/InvoiceHistoryScreen.kt', 'w') as f:
    f.write(history_code)

# Update Manage Items Screen
with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    manage_code = f.read()

manage_code = manage_code.replace('TopAppBar(', 'CenterAlignedTopAppBar(')
manage_code = manage_code.replace('Card(', 'ElevatedCard(')
manage_code = manage_code.replace('Button(', 'ElevatedButton(')
manage_code = manage_code.replace('FloatingActionButton(', 'ExtendedFloatingActionButton(')
manage_code = manage_code.replace('Icon(Icons.Default.Add, contentDescription = "Add Item")', 'text = { Text("Add Item") }, icon = { Icon(Icons.Default.Add, contentDescription = "Add Item") }')

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(manage_code)
