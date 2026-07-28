import re

# Update InvoiceDetailScreen.kt
with open('app/src/main/java/com/example/ui/screens/InvoiceDetailScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('                        }\n                        if (invoice.previousOutstanding > 0) {', '                        }\n                        Spacer(modifier = Modifier.height(8.dp))\n                        if (invoice.previousOutstanding > 0) {')

with open('app/src/main/java/com/example/ui/screens/InvoiceDetailScreen.kt', 'w') as f:
    f.write(content)

