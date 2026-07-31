import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

new_home_screen = """package com.example.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.viewmodel.InvoiceUiState
import java.util.Calendar
import java.text.SimpleDateFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    state: InvoiceUiState,
    onSyncClick: () -> Unit,
    onSettingsClick: () -> Unit,
    onNewInvoice: () -> Unit,
    onViewInvoices: () -> Unit
) {
    val todayMillis = Calendar.getInstance().apply {
        set(Calendar.HOUR_OF_DAY, 0)
        set(Calendar.MINUTE, 0)
        set(Calendar.SECOND, 0)
        set(Calendar.MILLISECOND, 0)
    }.timeInMillis
    
    val todayInvoices = state.invoiceHistory.filter { it.dateMillis >= todayMillis }.sortedByDescending { it.dateMillis }
    val todaySales = todayInvoices.sumOf { it.billAmount }
    val totalCustomers = state.customers.size
    
    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { 
                    Text(
                        text = state.storeName.ifBlank { "My Store" },
                        fontWeight = FontWeight.Bold
                    ) 
                },
                actions = {
                    IconButton(onClick = onSyncClick) {
                        Icon(Icons.Default.Refresh, contentDescription = "Sync Data")
                    }
                    IconButton(onClick = onSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                    titleContentColor = MaterialTheme.colorScheme.primary,
                )
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = onNewInvoice,
                icon = { Icon(Icons.Default.Add, contentDescription = "New Invoice") },
                text = { Text("New Invoice", fontWeight = FontWeight.Bold) },
                containerColor = MaterialTheme.colorScheme.primaryContainer,
                contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
                elevation = FloatingActionButtonDefaults.elevation(defaultElevation = 4.dp)
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            
            // Header Section
            item {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        text = "Welcome, ${state.ownerName.ifBlank { "Owner" }}!",
                        style = MaterialTheme.typography.headlineMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onBackground
                    )
                    Text(
                        text = "${state.storeAddress}${if (state.storePhone.isNotBlank()) " • ${state.storePhone}" else ""}",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            
            // Stats Section
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(), 
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    ElevatedCard(
                        modifier = Modifier.weight(1f),
                        colors = CardDefaults.elevatedCardColors(
                            containerColor = MaterialTheme.colorScheme.primaryContainer,
                            contentColor = MaterialTheme.colorScheme.onPrimaryContainer
                        ),
                        elevation = CardDefaults.elevatedCardElevation(defaultElevation = 0.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Icon(Icons.Default.TrendingUp, contentDescription = null, modifier = Modifier.size(28.dp))
                            Spacer(modifier = Modifier.height(16.dp))
                            Text("Today's Sales", style = MaterialTheme.typography.labelLarge)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                "${state.currencySymbol}${String.format(Locale.US, "%.2f", todaySales)}",
                                style = MaterialTheme.typography.headlineSmall,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                    
                    ElevatedCard(
                        modifier = Modifier.weight(1f),
                        colors = CardDefaults.elevatedCardColors(
                            containerColor = MaterialTheme.colorScheme.secondaryContainer,
                            contentColor = MaterialTheme.colorScheme.onSecondaryContainer
                        ),
                        elevation = CardDefaults.elevatedCardElevation(defaultElevation = 0.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Icon(Icons.Default.People, contentDescription = null, modifier = Modifier.size(28.dp))
                            Spacer(modifier = Modifier.height(16.dp))
                            Text("Total Customers", style = MaterialTheme.typography.labelLarge)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                "$totalCustomers",
                                style = MaterialTheme.typography.headlineSmall,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            }
            
            // View All Invoices Action
            item {
                OutlinedCard(
                    onClick = onViewInvoices,
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.outlinedCardColors(
                        containerColor = MaterialTheme.colorScheme.surface,
                    ),
                    border = CardDefaults.outlinedCardBorder(true)
                ) {
                    ListItem(
                        headlineContent = { Text("View All Invoices", fontWeight = FontWeight.Bold) },
                        supportingContent = { Text("${state.invoiceHistory.size} total invoices") },
                        leadingContent = {
                            Icon(
                                Icons.Default.ReceiptLong,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.primary
                            )
                        },
                        trailingContent = {
                            Icon(Icons.Default.ChevronRight, contentDescription = "Go to Invoices")
                        },
                        colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surface)
                    )
                }
            }
            
            // Recent Activity Section
            item {
                Text(
                    text = "Recent Activity (Today)", 
                    style = MaterialTheme.typography.titleLarge, 
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onBackground
                )
            }
            
            if (todayInvoices.isEmpty()) {
                item {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 32.dp), 
                        contentAlignment = Alignment.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Icon(Icons.Default.ReceiptLong, contentDescription = null, modifier = Modifier.size(48.dp), tint = MaterialTheme.colorScheme.surfaceVariant)
                            Text("No invoices generated today.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            } else {
                items(todayInvoices) { invoice ->
                    val timeFormat = SimpleDateFormat("hh:mm a", Locale.getDefault())
                    val timeString = timeFormat.format(invoice.dateMillis)
                    
                    ElevatedCard(
                        modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                        elevation = CardDefaults.elevatedCardElevation(defaultElevation = 1.dp),
                        colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface)
                    ) {
                        ListItem(
                            headlineContent = { Text(invoice.customerName, fontWeight = FontWeight.Bold) },
                            supportingContent = { Text("ID: ${invoice.invoiceId} • $timeString") },
                            trailingContent = { 
                                Text(
                                    "${state.currencySymbol}${String.format(Locale.US, "%.2f", invoice.billAmount)}", 
                                    fontWeight = FontWeight.Bold,
                                    style = MaterialTheme.typography.titleMedium,
                                    color = MaterialTheme.colorScheme.primary
                                ) 
                            },
                            leadingContent = {
                                Surface(
                                    shape = MaterialTheme.shapes.large,
                                    color = MaterialTheme.colorScheme.secondaryContainer,
                                    modifier = Modifier.size(48.dp)
                                ) {
                                    Box(contentAlignment = Alignment.Center) {
                                        Text(
                                            text = invoice.customerName.take(1).uppercase(),
                                            style = MaterialTheme.typography.titleMedium,
                                            fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.onSecondaryContainer
                                        )
                                    }
                                }
                            },
                            colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surface)
                        )
                    }
                }
            }
            
            // Extra padding at bottom for FAB
            item {
                Spacer(modifier = Modifier.height(72.dp))
            }
        }
    }
}
"""

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(new_home_screen)

