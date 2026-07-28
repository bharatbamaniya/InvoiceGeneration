import re

with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("onSkipToCheckout: () -> Unit", "")
content = content.replace("onSkipToCheckout = {\n                            viewModel.selectCustomer(null)\n                            currentScreen = AppScreen.CHECKOUT\n                        }", "")

old_top_bar = """            TopAppBar(
                title = { Text("Select Customer") },
                actions = {
                    TextButton(onClick = onSkipToCheckout) {
                        Text("Skip")
                    }
                }
            )"""
new_top_bar = """            TopAppBar(
                title = { Text("Customers") }
            )"""

content = content.replace(old_top_bar, new_top_bar)

with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'w') as f:
    f.write(content)

