package com.example.ui.screens

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.viewmodel.InvoiceUiState
import java.util.Calendar
import java.text.SimpleDateFormat
import java.util.Locale
import java.util.Date

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    state: InvoiceUiState,
    onSyncClick: () -> Unit,
    onSettingsClick: () -> Unit,
    onNewInvoice: () -> Unit,
    onViewInvoices: () -> Unit,
    onManageItems: () -> Unit
) {
    val todayMillis = Calendar.getInstance().apply {
        set(Calendar.HOUR_OF_DAY, 0)
        set(Calendar.MINUTE, 0)
        set(Calendar.SECOND, 0)
        set(Calendar.MILLISECOND, 0)
    }.timeInMillis

    val todayInvoices = state.invoiceHistory.filter { it.dateMillis >= todayMillis }
    val todaySales = todayInvoices.sumOf { it.billAmount }
    val totalCustomers = state.customers.size
    val pendingAmount = state.customers.sumOf { if (it.balance > 0) it.balance else 0.0 }
    val pendingCustomersCount = state.customers.count { it.balance > 0 }
    
    // Calculate received amount today
    val receivedToday = todayInvoices.sumOf { it.billAmount - (it.totalBalance - it.previousOutstanding) }

    val yesterdayMillis = todayMillis - 86400000L
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


    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Text(
                        text = "Overview",
                        fontWeight = FontWeight.Bold,
                        fontSize = 24.sp
                    ) 
                },
                actions = {
                    IconButton(onClick = onManageItems) {
                        Icon(Icons.Default.Inventory2, contentDescription = "Manage Items")
                    }
                    IconButton(onClick = onViewInvoices) {
                        Icon(Icons.Default.History, contentDescription = "History")
                    }
                    IconButton(onClick = onSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                    titleContentColor = MaterialTheme.colorScheme.onBackground,
                    actionIconContentColor = MaterialTheme.colorScheme.onSurfaceVariant
                )
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                modifier = Modifier.padding(bottom = 88.dp),
                onClick = onNewInvoice,
                icon = { Icon(Icons.Default.Add, contentDescription = "New Invoice") },
                text = { Text("New Invoice", fontWeight = FontWeight.Normal) },
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary,
                shape = RoundedCornerShape(16.dp),
                elevation = FloatingActionButtonDefaults.elevation(defaultElevation = 4.dp)
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 100.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            
            // 4 Grid Cards
            item {
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(), 
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        StatCard(
                            modifier = Modifier.weight(1f),
                            title = "TODAY'S SALES",
                            value = "${state.currencySymbol}${String.format(Locale.US, "%.0f", todaySales)}",
                            trendIcon = salesTrendIcon,
                            trendText = salesTrendStr
                        )
                        StatCard(
                            modifier = Modifier.weight(1f),
                            title = "ACTIVE CUSTOMERS",
                            value = "$totalCustomers",
                            trendIcon = Icons.AutoMirrored.Filled.TrendingUp,
                            trendText = activeCustomersStr
                        )
                    }
                    Row(
                        modifier = Modifier.fillMaxWidth(), 
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        StatCard(
                            modifier = Modifier.weight(1f),
                            title = "RECEIVED",
                            value = "${state.currencySymbol}${String.format(Locale.US, "%.0f", receivedToday)}",
                            trendIcon = receivedTrendIcon,
                            trendText = receivedTrendStr
                        )
                        StatCard(
                            modifier = Modifier.weight(1f),
                            title = "PENDING",
                            value = "${state.currencySymbol}${String.format(Locale.US, "%.0f", pendingAmount)}",
                            trendIcon = Icons.Default.Schedule,
                            trendText = "$pendingCustomersCount customer(s)"
                        )
                    }
                }
            }
            
            // Weekly Sales Trend
            item {
                Text(
                    text = "Weekly Sales Trend", 
                    style = MaterialTheme.typography.titleLarge, 
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(top = 8.dp)
                )
                
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 12.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Total Revenue (7 Days)", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        val totalRevenue = state.invoiceHistory.filter { System.currentTimeMillis() - it.dateMillis <= 7 * 24 * 60 * 60 * 1000L }.sumOf { it.billAmount }
                        Text(
                            "${state.currencySymbol}${String.format(Locale.US, "%.0f", totalRevenue)}", 
                            style = MaterialTheme.typography.headlineLarge, 
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(top = 4.dp, bottom = 16.dp)
                        )
                        
                        // Custom Chart
                        Box(modifier = Modifier.fillMaxWidth().height(150.dp)) {
                            ChartCurve(color = MaterialTheme.colorScheme.primary, dataPoints = weeklySales)
                        }
                        
                        val daysList = mutableListOf<String>()
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
                        }
                    }
                }
            }
            
            // Top Performing Items
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            "Top Performing Items", 
                            style = MaterialTheme.typography.titleMedium, 
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(bottom = 16.dp)
                        )
                        
                        val itemCounts = state.invoiceHistory.flatMap { it.items }.groupBy { it.item.name }.mapValues { it.value.sumOf { item -> item.quantity } }
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
                        }
                    }
                }
            }
            
            // Customer Growth
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            "Customer Growth", 
                            style = MaterialTheme.typography.titleMedium, 
                            fontWeight = FontWeight.Bold
                        )
                        Column(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                "${state.customers.size} Total", 
                                style = MaterialTheme.typography.headlineMedium, 
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                "Registered customers", 
                                style = MaterialTheme.typography.labelMedium, 
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(top = 4.dp)
                            )
                        }
                        
                        Box(modifier = Modifier.fillMaxWidth().height(60.dp)) {
                            ChartCurve(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), simple = true, dataPoints = weeklyCustomers)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun StatCard(modifier: Modifier = Modifier, title: String, value: String, trendIcon: androidx.compose.ui.graphics.vector.ImageVector, trendText: String) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f)),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(title, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
            Text(
                value, 
                style = MaterialTheme.typography.titleLarge, 
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(vertical = 6.dp)
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(trendIcon, contentDescription = null, modifier = Modifier.size(14.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(modifier = Modifier.width(4.dp))
                Text(trendText, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
fun ProgressBarItem(title: String, percentage: String, progress: Float) {
    Column {
        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = 6.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(title, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onBackground)
            Text(percentage, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onBackground)
        }
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(6.dp)
                .background(MaterialTheme.colorScheme.surface, RoundedCornerShape(3.dp))
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth(progress)
                    .height(6.dp)
                    .background(MaterialTheme.colorScheme.primary, RoundedCornerShape(3.dp))
            )
        }
    }
}

@Composable
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
}