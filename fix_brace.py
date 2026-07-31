import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("Icon(Icons.Default.Edit, contentDescription = \"Edit\", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)\n                }\n        },", "Icon(Icons.Default.Edit, contentDescription = \"Edit\", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)\n                }\n            }\n        },")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

