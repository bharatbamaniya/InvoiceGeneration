import re

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    code = f.read()

# Fix ExtendedFloatingActionButton syntax
old_fab = """            ExtendedFloatingActionButton(onClick = {
                editingItem = null
                showDialog = true
            }) {
                text = { Text("Add Item") }, icon = { Icon(Icons.Default.Add, contentDescription = "Add Item") }
            }"""
            
new_fab = """            ExtendedFloatingActionButton(
                onClick = {
                    editingItem = null
                    showDialog = true
                },
                text = { Text("Add Item") },
                icon = { Icon(Icons.Default.Add, contentDescription = "Add Item") }
            )"""

code = code.replace(old_fab, new_fab)

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(code)
