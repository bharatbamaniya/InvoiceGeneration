import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

# 1. Add trend calculations
trend_calcs = """    val yesterdayMillis = todayMillis - 86400000L
    val yesterdayInvoices = state.invoiceHistory.filter { it.dateMillis in yesterdayMillis until todayMillis }
    val yesterdaySales = yesterdayInvoices.sumOf { it.billAmount }
    val salesTrend = if (yesterdaySales > 0) ((todaySales - yesterdaySales) / yesterdaySales) * 100 else if (todaySales > 0) 100.0 else 0.0
    val salesTrendStr = if (salesTrend >= 0) "+${String.format(Locale.US, "%.0f", salesTrend)}% vs yesterday" else "${String.format(Locale.US, "%.0f", salesTrend)}% vs yesterday"
    val salesTrendIcon = if (salesTrend >= 0) Icons.AutoMirrored.Filled.TrendingUp else Icons.AutoMirrored.Filled.TrendingDown

    val yesterdayReceived = yesterdayInvoices.sumOf { it.billAmount - (it.totalBalance - it.previousOutstanding) }
    val receivedTrend = if (yesterdayReceived > 0) ((receivedToday - yesterdayReceived) / yesterdayReceived) * 100 else if (receivedToday > 0) 100.0 else 0.0
    val receivedTrendStr = if (receivedTrend >= 0) "+${String.format(Locale.US, "%.0f", receivedTrend)}% vs yesterday" else "${String.format(Locale.US, "%.0f", receivedTrend)}% vs yesterday"
    val receivedTrendIcon = if (receivedTrend >= 0) Icons.AutoMirrored.Filled.TrendingUp else Icons.AutoMirrored.Filled.TrendingDown

    val activeCustomersCount = state.invoiceHistory.mapNotNull { it.customerId }.distinct().size
    val activeCustomersStr = "$activeCustomersCount active"
    
    // Weekly sales points
    val weeklySales = FloatArray(7)
    for (i in 6 downTo 0) {
        val startOfDay = todayMillis - (i * 86400000L)
        val endOfDay = startOfDay + 86400000L
        val daySales = state.invoiceHistory
            .filter { it.dateMillis in startOfDay until endOfDay }
            .sumOf { it.billAmount }
        weeklySales[6 - i] = daySales.toFloat()
    }
"""
text = text.replace("val receivedToday = todayInvoices.sumOf { it.billAmount - (it.totalBalance - it.previousOutstanding) }", "val receivedToday = todayInvoices.sumOf { it.billAmount - (it.totalBalance - it.previousOutstanding) }\n\n" + trend_calcs)

# 2. Replace static trend texts
text = text.replace('trendIcon = Icons.AutoMirrored.Filled.TrendingUp,\n                            trendText = "+15% vs yesterday"', 'trendIcon = salesTrendIcon,\n                            trendText = salesTrendStr')
text = text.replace('trendText = "+5% this week"', 'trendText = activeCustomersStr')
text = text.replace('trendIcon = Icons.AutoMirrored.Filled.TrendingUp,\n                            trendText = "+8% this week"', 'trendIcon = receivedTrendIcon,\n                            trendText = receivedTrendStr')
text = text.replace('trendText = "$pendingCustomersCount customer"', 'trendText = "$pendingCustomersCount customer(s)"')

# 3. Replace Customer Growth static numbers
text = text.replace('"+42 New"', '"${state.customers.size} Total"')
text = text.replace('"Total registered customers"', '"Registered customers"')

# 4. Make ChartCurve dynamic
chart_curve_code = """@Composable
fun ChartCurve(color: Color, simple: Boolean = false, dataPoints: FloatArray = FloatArray(7) { 0f }) {
    Canvas(modifier = Modifier.fillMaxSize()) {
        val path = Path()
        val width = size.width
        val height = size.height
        
        val maxPoint = dataPoints.maxOrNull() ?: 1f
        val maxVal = if (maxPoint <= 0f) 1f else maxPoint
        
        if (dataPoints.isEmpty() || dataPoints.all { it == 0f }) {
            // Flat line if no data
            path.moveTo(0f, height * 0.9f)
            path.lineTo(width, height * 0.9f)
        } else {
            val stepX = width / (dataPoints.size - 1).coerceAtLeast(1)
            
            for (i in dataPoints.indices) {
                val x = i * stepX
                val normalizedY = 1f - (dataPoints[i] / maxVal)
                val y = height * (0.1f + 0.8f * normalizedY)
                
                if (i == 0) {
                    path.moveTo(x, y)
                } else {
                    val prevX = (i - 1) * stepX
                    val prevNormalizedY = 1f - (dataPoints[i - 1] / maxVal)
                    val prevY = height * (0.1f + 0.8f * prevNormalizedY)
                    
                    val controlX1 = prevX + (x - prevX) / 2
                    val controlX2 = prevX + (x - prevX) / 2
                    
                    path.cubicTo(controlX1, prevY, controlX2, y, x, y)
                }
            }
        }
        
        drawPath(
            path = path,
            color = color,
            style = Stroke(width = 4.dp.toPx(), cap = StrokeCap.Round)
        )
        
        if (!simple) {
            val fillPath = Path()
            fillPath.addPath(path)
            fillPath.lineTo(width, height)
            fillPath.lineTo(0f, height)
            fillPath.close()
            
            drawPath(
                path = fillPath,
                brush = Brush.verticalGradient(
                    colors = listOf(color.copy(alpha = 0.3f), Color.Transparent),
                    startY = 0f,
                    endY = height
                )
            )
        }
    }
}"""
# We need to replace the entire ChartCurve method.
start_chart = text.find("@Composable\nfun ChartCurve")
if start_chart != -1:
    text = text[:start_chart] + chart_curve_code

# Also update the calls to ChartCurve to pass weeklySales
text = text.replace("ChartCurve(color = MaterialTheme.colorScheme.primary)", "ChartCurve(color = MaterialTheme.colorScheme.primary, dataPoints = weeklySales)")
text = text.replace("ChartCurve(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), simple = true)", "ChartCurve(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), simple = true, dataPoints = weeklySales)")

# Weekly labels fix to show actual days
# Let's generate short day names
days_calc = """                        val daysList = mutableListOf<String>()
                        val sdf = SimpleDateFormat("EEE", Locale.US)
                        for (i in 6 downTo 0) {
                            daysList.add(sdf.format(Date(todayMillis - (i * 86400000L))))
                        }
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            daysList.forEach {
                                Text(it, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }"""
# Find the Row with listOf("Mon", "Tue"...
row_start = text.find("Row(\n                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp),\n                            horizontalArrangement = Arrangement.SpaceBetween\n                        ) {")
if row_start != -1:
    row_end = text.find("                        }", row_start) + 25
    # Replace that part
    text = text[:row_start] + days_calc + text[row_end:]

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

