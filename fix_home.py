import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    home = f.read()

# Fix Total Revenue
home = home.replace(
    'Text(\n                            "${state.currencySymbol}8,450",',
    'val totalRevenue = state.invoiceHistory.filter { System.currentTimeMillis() - it.dateMillis <= 7 * 24 * 60 * 60 * 1000L }.sumOf { it.billAmount }\n                        Text(\n                            "${state.currencySymbol}${String.format(Locale.US, "%.0f", totalRevenue)}",'
)

# Fix Top Performing Items
# I'll compute top 3 items from invoiceHistory.
old_top_items = """                        ProgressBarItem("Artisan Coffee Beans", "35%", 0.7f)
                        Spacer(modifier = Modifier.height(16.dp))
                        ProgressBarItem("Organic Avocados", "22%", 0.44f)
                        Spacer(modifier = Modifier.height(16.dp))
                        ProgressBarItem("Sourdough Loaf", "15%", 0.3f)"""

new_top_items = """                        val itemCounts = state.invoiceHistory.flatMap { it.items }.groupBy { it.item.name }.mapValues { it.value.sumOf { item -> item.quantity } }
                        val topItems = itemCounts.entries.sortedByDescending { it.value }.take(3)
                        val totalQty = itemCounts.values.sum().coerceAtLeast(1.0)
                        
                        if (topItems.isEmpty()) {
                            Text("No items sold yet", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        } else {
                            topItems.forEachIndexed { index, entry ->
                                val percentage = (entry.value / totalQty) * 100
                                ProgressBarItem(entry.key, "${String.format(Locale.US, "%.0f", percentage)}%", (entry.value / totalQty).toFloat())
                                if (index < topItems.size - 1) {
                                    Spacer(modifier = Modifier.height(16.dp))
                                }
                            }
                        }"""

home = home.replace(old_top_items, new_top_items)

# Fix Customer Growth
old_growth = """                            Text(
                                "+42 New", 
                                 style = MaterialTheme.typography.headlineMedium,"""

new_growth = """                            val recentCustomers = state.customers.size // we can just show total customers for now as we don't have creation dates for them
                            Text(
                                "${recentCustomers} Total", 
                                 style = MaterialTheme.typography.headlineMedium,"""

home = home.replace(old_growth, new_growth)
home = home.replace(
    '"This week vs last week",',
    '"Total registered customers",'
)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(home)

