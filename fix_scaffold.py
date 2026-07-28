import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    content = f.read()

scaffold_content = """    val totalBalance = state.cartItems.sumOf { it.customPrice * it.quantity }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    val customerName = if (state.selectedCustomerId != null) {
                        state.customers.find { it.id == state.selectedCustomerId }?.name ?: "Unknown Customer"
                    } else {
                        "Unknown Customer"
                    }
                    Column {
                        Text(
                            text = customerName,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "New Invoice",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                actions = {
                    IconButton(
                        onClick = onManageItems,
                        modifier = Modifier.testTag("manage_items_button")
                    ) {
                        Icon(imageVector = Icons.Default.Inventory, contentDescription = "Manage Items")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f)
                )
            )
        },
        floatingActionButton = {
            // Cart Summary Floating Action Button
            val hideCheckoutBar = isSearchFocused && WindowInsets.isImeVisible
            if (state.cartItems.isNotEmpty() && !hideCheckoutBar) {
                androidx.compose.material3.ExtendedFloatingActionButton(
                    onClick = { showCheckoutSheet = true },
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary,
                    icon = { Icon(Icons.Default.ShoppingCart, contentDescription = "Checkout") },
                    text = { 
                        Text(
                            text = String.format(Locale.US, "Checkout • %s%.2f", state.currencySymbol, totalBalance),
                            fontWeight = FontWeight.Bold
                        ) 
                    }
                )
            }
        }
    ) { innerPadding ->"""

content = re.sub(r'val allAvailableItems = state\.inventoryItems.*?\)\s*\{\s*innerPadding ->', 'val allAvailableItems = state.inventoryItems\n\n' + scaffold_content, content, flags=re.DOTALL)
    
with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(content)
