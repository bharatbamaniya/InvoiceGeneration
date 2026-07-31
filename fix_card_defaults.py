import os
import re

files = [
    'app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt',
    'app/src/main/java/com/example/ui/screens/InvoiceHistoryScreen.kt'
]

for file in files:
    with open(file, 'r') as f:
        code = f.read()
    
    code = code.replace('ElevatedCardDefaults', 'CardDefaults')
    code = code.replace('CardDefaults.cardColors', 'CardDefaults.elevatedCardColors')
    
    with open(file, 'w') as f:
        f.write(code)

