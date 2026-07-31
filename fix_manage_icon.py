import re

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    text = f.read()

replacement = """                                Box(contentAlignment = Alignment.Center) {
                                    if (item.iconEmoji.startsWith("content://") || item.iconEmoji.startsWith("http")) {
                                        AsyncImage(
                                            model = item.iconEmoji,
                                            contentDescription = item.name,
                                            contentScale = ContentScale.Crop,
                                            modifier = Modifier.fillMaxSize()
                                        )
                                    } else {
                                        Text(
                                            item.name.take(1).uppercase(), 
                                            fontWeight = FontWeight.Bold,
                                            style = MaterialTheme.typography.titleMedium,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }
                                }"""

text = text.replace("""                                Box(contentAlignment = Alignment.Center) {
                                    Text(
                                        item.name.take(1).uppercase(), 
                                        fontWeight = FontWeight.Bold,
                                        style = MaterialTheme.typography.titleMedium,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }""", replacement)

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(text)

