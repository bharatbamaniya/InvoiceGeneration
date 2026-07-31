import re

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    text = f.read()

old_item_block = """                items(filteredItems) { item ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(bottom = 12.dp)
                            .clickable { 
                                editingItem = item
                                showDialog = true
                            },"""

new_item_block = """                items(filteredItems, key = { it.id }) { item ->
                    val dismissState = rememberSwipeToDismissBoxState(
                        confirmValueChange = {
                            if (it == SwipeToDismissBoxValue.EndToStart) {
                                onDeleteItem(item.id)
                                true
                            } else false
                        }
                    )
                    SwipeToDismissBox(
                        state = dismissState,
                        enableDismissFromStartToEnd = false,
                        backgroundContent = {
                            Box(
                                Modifier
                                    .fillMaxWidth()
                                    .padding(bottom = 12.dp)
                                    .background(MaterialTheme.colorScheme.error, RoundedCornerShape(12.dp))
                                    .padding(horizontal = 20.dp),
                                contentAlignment = Alignment.CenterEnd
                            ) {
                                Icon(Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.onError)
                            }
                        },
                        content = {
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(bottom = 12.dp)
                                    .clickable { 
                                        editingItem = item
                                        showDialog = true
                                    },"""

text = text.replace(old_item_block, new_item_block)
text = text.replace("                        }\n                    }\n                }", "                        }\n                    }\n                }\n                }")

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(text)

