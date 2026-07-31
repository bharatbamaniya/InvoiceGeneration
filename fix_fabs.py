import os
import re

# Fix HomeScreen
with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    home_code = f.read()

home_code = home_code.replace('ExtendedFloatingActionButton(\n                onClick = onNewInvoice,',
                              'ExtendedFloatingActionButton(\n                modifier = Modifier.padding(bottom = 88.dp),\n                onClick = onNewInvoice,')

home_code = home_code.replace('contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)',
                              'contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 100.dp)')

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(home_code)


# Fix CustomersScreen
with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'r') as f:
    cust_code = f.read()

cust_code = cust_code.replace('FloatingActionButton(onClick = { showAddDialog = true }) {',
                              'FloatingActionButton(onClick = { showAddDialog = true }, modifier = Modifier.padding(bottom = 88.dp)) {')

cust_code = cust_code.replace('contentPadding = PaddingValues(16.dp)',
                              'contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 16.dp, bottom = 100.dp)')

with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'w') as f:
    f.write(cust_code)

