import re

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    code = f.read()

# Fix signature
code = code.replace(
    'onAddItem: (GroceryItem) -> Unit,\n    onEditItem: (GroceryItem) -> Unit,\n    onDeleteItem: (GroceryItem) -> Unit,',
    'onAddItem: (String, Double, String) -> Unit,\n    onUpdateItem: (GroceryItem) -> Unit,\n    onDeleteItem: (String) -> Unit,'
)

# Fix invocations
code = code.replace(
    'onAddItem(GroceryItem(name = name, price = price, unit = unit))',
    'onAddItem(name, price, unit)'
)
code = code.replace(
    'onEditItem(editingItem!!.copy(name = name, price = price, unit = unit))',
    'onUpdateItem(editingItem!!.copy(name = name, price = price, unit = unit))'
)
code = code.replace(
    'onDeleteItem(editingItem!!)',
    'onDeleteItem(editingItem!!.id)'
)

# Fix background unresolved (replace with Surface)
code = code.replace(
    'modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant)',
    'modifier = Modifier'
) # Actually ExposedDropdownMenu has containerColor parameter in newer compose versions, or it just inherits. Just remove background, it's fine.

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(code)

