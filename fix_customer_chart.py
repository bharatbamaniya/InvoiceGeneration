import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

customer_array = """
    // Weekly customer active points
    val weeklyCustomers = FloatArray(7)
    for (i in 6 downTo 0) {
        val startOfDay = todayMillis - (i * 86400000L)
        val endOfDay = startOfDay + 86400000L
        val dayCust = state.invoiceHistory
            .filter { it.dateMillis in startOfDay until endOfDay }
            .mapNotNull { it.customerId }.distinct().size
        weeklyCustomers[6 - i] = dayCust.toFloat()
    }
"""

text = text.replace("// Weekly sales points", customer_array + "\n    // Weekly sales points")
text = text.replace("ChartCurve(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), simple = true, dataPoints = weeklySales)", "ChartCurve(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), simple = true, dataPoints = weeklyCustomers)")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

