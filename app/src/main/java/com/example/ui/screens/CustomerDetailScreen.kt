package com.example.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.model.Customer
import com.example.model.Invoice
import com.example.model.Payment
import androidx.compose.ui.graphics.Color
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CustomerDetailScreen(
    customer: Customer,
    invoices: List<Invoice>,
    payments: List<Payment>,
    currencySymbol: String,
    onBack: () -> Unit,
    onNewInvoice: () -> Unit,
    onSettleBalance: (amount: Double, remark: String) -> Unit,
    onViewInvoice: (Invoice) -> Unit
) {
    var showSettleDialog by remember { mutableStateOf(false) }
    var settleAmount by remember { mutableStateOf("") }
    var settleRemark by remember { mutableStateOf("") }

    val dateFormat = remember { SimpleDateFormat("dd MMM yyyy, hh:mm a", Locale.getDefault()) }
    
    val ledger = remember(invoices, payments) {
        val ledgerInvoices = invoices.map { LedgerItem.InvoiceItem(it) }
        val ledgerPayments = payments.map { LedgerItem.PaymentItem(it) }
        (ledgerInvoices + ledgerPayments).sortedByDescending { it.dateMillis }
    }


    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(customer.name) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = onNewInvoice,
                icon = { Icon(Icons.Default.Add, contentDescription = null) },
                text = { Text("New Invoice") }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp)
        ) {
            Card(
                modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
            ) {
                Row(
                    modifier = Modifier.padding(16.dp).fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("Outstanding Balance", style = MaterialTheme.typography.titleMedium)
                        if (customer.balance > 0) {
                            Button(onClick = { showSettleDialog = true }) {
                                Text("Settle Balance")
                            }
                        }
                    }
                    Text(
                        "$currencySymbol${String.format("%.2f", customer.balance)}",
                        style = MaterialTheme.typography.headlineMedium,
                        fontWeight = FontWeight.Bold,
                        color = if (customer.balance > 0) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
            }
            
            Text("Transaction Ledger", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(8.dp))
            
            if (ledger.isEmpty()) {
                Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                    Text("No transactions yet.")
                }
            } else {
                LazyColumn(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(ledger) { entry ->
                        when(entry) {
                            is LedgerItem.InvoiceItem -> {
                                Card(
                                    modifier = Modifier.fillMaxWidth().clickable { onViewInvoice(entry.invoice) },
                                ) {
                                    Row(
                                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Column {
                                            Text(entry.invoice.invoiceId, fontWeight = FontWeight.Bold)
                                            Text(dateFormat.format(Date(entry.dateMillis)), style = MaterialTheme.typography.bodySmall)
                                        }
                                        Text("+ $currencySymbol${String.format("%.2f", entry.invoice.billAmount)}", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.error)
                                    }
                                }
                            }
                            is LedgerItem.PaymentItem -> {
                                Card(
                                    modifier = Modifier.fillMaxWidth(),
                                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.tertiaryContainer)
                                ) {
                                    Row(
                                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Column {
                                            Text("Payment Received", fontWeight = FontWeight.Bold)
                                            Text(dateFormat.format(Date(entry.dateMillis)), style = MaterialTheme.typography.bodySmall)
                                            if (entry.payment.remark.isNotBlank()) {
                                                Text("Remark: ${entry.payment.remark}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onTertiaryContainer.copy(alpha = 0.7f))
                                            }
                                        }
                                        Text("- $currencySymbol${String.format("%.2f", entry.payment.amount)}", fontWeight = FontWeight.Bold, color = Color(0xFF2E7D32)) // Dark green
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        if (showSettleDialog) {
            AlertDialog(
                onDismissRequest = { showSettleDialog = false },
                title = { Text("Settle Balance") },
                text = {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("Enter the amount received from ${customer.name}.")
                        OutlinedTextField(
                            value = settleAmount,
                            onValueChange = { settleAmount = it },
                            label = { Text("Amount ($currencySymbol)") },
                            singleLine = true
                        )
                        OutlinedTextField(
                            value = settleRemark,
                            onValueChange = { settleRemark = it },
                            label = { Text("Remark (Optional)") },
                            singleLine = true
                        )
                    }
                },
                confirmButton = {
                    Button(onClick = {
                        val amount = settleAmount.toDoubleOrNull()
                        if (amount != null && amount > 0) {
                            onSettleBalance(amount, settleRemark)
                            showSettleDialog = false
                            settleAmount = ""
                            settleRemark = ""
                        }
                    }) {
                        Text("Settle")
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showSettleDialog = false }) {
                        Text("Cancel")
                    }
                }
            )
        }
    }
}

sealed class LedgerItem {
    abstract val dateMillis: Long
    data class InvoiceItem(val invoice: Invoice) : LedgerItem() {
        override val dateMillis = invoice.dateMillis
    }
    data class PaymentItem(val payment: Payment) : LedgerItem() {
        override val dateMillis = payment.dateMillis
    }
}
