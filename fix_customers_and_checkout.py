import re

# Fix CustomersScreen
with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'r') as f:
    customers_code = f.read()

customers_code = customers_code.replace(
    'Row(\n                            modifier = Modifier.padding(16.dp),',
    'Row(\n                            modifier = Modifier.fillMaxWidth().padding(16.dp),'
)

# Use ElevatedCard for more Material UI feel on Customers Screen
customers_code = customers_code.replace('Card(', 'ElevatedCard(')

with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'w') as f:
    f.write(customers_code)

# Fix CheckoutScreen
with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    checkout_code = f.read()

# Add onBack
if "onBack: () -> Unit" not in checkout_code:
    checkout_code = checkout_code.replace(
        'onManageItems: () -> Unit\n) {',
        'onManageItems: () -> Unit,\n    onBack: () -> Unit\n) {'
    )

# Add navigationIcon
if 'navigationIcon = {' not in checkout_code:
    checkout_code = checkout_code.replace(
        'TopAppBar(\n                title = {',
        'TopAppBar(\n                navigationIcon = {\n                    IconButton(onClick = onBack) {\n                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")\n                    }\n                },\n                title = {'
    )

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(checkout_code)

# Fix MainActivity to pass onBack to CheckoutScreen
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main_code = f.read()

if "onBack = { currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.CUSTOMERS }" not in main_code:
    main_code = main_code.replace(
        'onManageItems = {\n                            currentScreen = AppScreen.MANAGE_ITEMS\n                        }\n                    )',
        'onManageItems = {\n                            currentScreen = AppScreen.MANAGE_ITEMS\n                        },\n                        onBack = { currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.CUSTOMERS }\n                    )'
    )
    
# Fix Floating Bottom Bar in MainActivity
old_bottom_bar = """        bottomBar = {
            if (currentScreen in listOf(AppScreen.HOME, AppScreen.CUSTOMERS)) {
                NavigationBar {
                    NavigationBarItem(
                        selected = currentScreen == AppScreen.HOME,
                        onClick = { currentScreen = AppScreen.HOME },
                        icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                        label = { Text("Home") }
                    )
                    NavigationBarItem(
                        selected = currentScreen == AppScreen.CUSTOMERS,
                        onClick = { currentScreen = AppScreen.CUSTOMERS },
                        icon = { Icon(Icons.Default.Person, contentDescription = "Customers") },
                        label = { Text("Customers") }
                    )
                }
            }
        }"""
        
new_bottom_bar = """        bottomBar = {
            if (currentScreen in listOf(AppScreen.HOME, AppScreen.CUSTOMERS)) {
                Box(
                    modifier = Modifier.fillMaxWidth().padding(16.dp).padding(bottom = 8.dp),
                    contentAlignment = Alignment.BottomCenter
                ) {
                    NavigationBar(
                        modifier = Modifier
                            .fillMaxWidth(0.6f)
                            .clip(androidx.compose.foundation.shape.RoundedCornerShape(32.dp)),
                        tonalElevation = 8.dp
                    ) {
                        NavigationBarItem(
                            selected = currentScreen == AppScreen.HOME,
                            onClick = { currentScreen = AppScreen.HOME },
                            icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                            label = { Text("Home") }
                        )
                        NavigationBarItem(
                            selected = currentScreen == AppScreen.CUSTOMERS,
                            onClick = { currentScreen = AppScreen.CUSTOMERS },
                            icon = { Icon(Icons.Default.Person, contentDescription = "Customers") },
                            label = { Text("Customers") }
                        )
                    }
                }
            }
        }"""
        
main_code = main_code.replace(old_bottom_bar, new_bottom_bar)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main_code)
