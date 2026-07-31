package com.example

import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.clickable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.CardDefaults

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Alignment
import androidx.compose.ui.draw.clip

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.activity.compose.BackHandler
import com.example.model.AppDatabase
import com.example.model.GroceryRepository
import com.example.model.Invoice
import com.example.ui.screens.CheckoutScreen
import com.example.ui.screens.InvoiceDetailScreen
import com.example.ui.screens.InvoiceHistoryScreen
import com.example.ui.screens.ManageItemsScreen
import com.example.ui.screens.CustomersScreen
import com.example.ui.screens.CustomerDetailScreen
import com.example.ui.theme.MyApplicationTheme
import com.example.viewmodel.InvoiceViewModel
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Icon
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Settings
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.Box
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import com.example.ui.screens.AuthScreen
import com.example.ui.screens.HomeScreen
import com.example.ui.screens.SettingsScreen

class InvoiceViewModelFactory(private val repository: GroceryRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(InvoiceViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return InvoiceViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}

enum class AppScreen {
    HOME,
    SETTINGS,
    CUSTOMERS,
    CUSTOMER_DETAIL,
    CHECKOUT,
    INVOICE_DETAIL,
    INVOICE_HISTORY,
    MANAGE_ITEMS
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    GroceryInvoiceApp()
                }
            }
        }
    }
}
@Composable
fun GroceryInvoiceApp() {
    val context = LocalContext.current
    val database = AppDatabase.getDatabase(context)
    val repository = GroceryRepository(database, context.applicationContext)
    val viewModel: InvoiceViewModel = viewModel(factory = InvoiceViewModelFactory(repository))
    val uiState by viewModel.uiState.collectAsState()
    
    var currentScreen by remember { mutableStateOf(AppScreen.HOME) }
    var selectedInvoiceForView by remember { mutableStateOf<Invoice?>(null) }
    
    BackHandler(enabled = currentScreen != AppScreen.HOME) {
        when (currentScreen) {
            AppScreen.CUSTOMER_DETAIL -> currentScreen = AppScreen.CUSTOMERS
            AppScreen.CHECKOUT -> currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.HOME
            AppScreen.INVOICE_DETAIL -> currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.HOME
            AppScreen.INVOICE_HISTORY -> currentScreen = AppScreen.HOME
            AppScreen.MANAGE_ITEMS -> currentScreen = AppScreen.CHECKOUT
            AppScreen.SETTINGS -> currentScreen = AppScreen.HOME
            AppScreen.CUSTOMERS -> currentScreen = AppScreen.HOME
            else -> currentScreen = AppScreen.HOME
        }
    }
    
    if (!uiState.isAuthenticated) {
        AuthScreen(onLogin = viewModel::login)
        return
    }

    Scaffold(
        // Bottom bar removed from scaffold to float freely
    ) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
            when (currentScreen) {
                AppScreen.HOME -> {
                    HomeScreen(
                        state = uiState,
                        onSyncClick = { viewModel.syncData() },
                        onSettingsClick = { currentScreen = AppScreen.SETTINGS },
                        onNewInvoice = {
                            viewModel.clearCart()
                            currentScreen = AppScreen.CUSTOMERS 
                        },
                        onViewInvoices = { currentScreen = AppScreen.INVOICE_HISTORY }, onManageItems = { currentScreen = AppScreen.MANAGE_ITEMS }
                    )
                }
                AppScreen.SETTINGS -> {
                    SettingsScreen(
                        state = uiState,
                        onUpdateStoreSettings = { name, address, phone, owner, swipe -> viewModel.updateStoreSettings(name, address, phone, owner, swipe) },
                        onLogout = { viewModel.logout() },
                        onBack = { currentScreen = AppScreen.HOME }
                    )
                }
                AppScreen.CUSTOMERS -> {
                    CustomersScreen(
                        customers = uiState.customers,
                        currencySymbol = uiState.currencySymbol,
                        onCustomerClick = { customer ->
                            viewModel.selectCustomer(customer.id)
                            currentScreen = AppScreen.CUSTOMER_DETAIL
                        },
                        onAddCustomer = viewModel::addCustomer,
                        
                    )
                }
                AppScreen.CUSTOMER_DETAIL -> {
                    val customer = uiState.customers.find { it.id == uiState.selectedCustomerId }
                    if (customer != null) {
                        CustomerDetailScreen(
                            customer = customer,
                            invoices = uiState.invoiceHistory.filter { it.customerId == customer.id }, payments = uiState.payments.filter { it.customerId == customer.id },
                            
                            currencySymbol = uiState.currencySymbol,
                            onBack = { currentScreen = AppScreen.CUSTOMERS },
                            onNewInvoice = { 
                                viewModel.clearCart()
                                currentScreen = AppScreen.CHECKOUT 
                            },
                            onSettleBalance = { cust, amount -> viewModel.settleCustomerBalance(cust.id, amount, "Settled from detail") },
                            
                        )
                    } else {
                        currentScreen = AppScreen.CUSTOMERS
                    }
                }
                AppScreen.CHECKOUT -> {
                    CheckoutScreen(
                        state = uiState,
                        defaultItems = viewModel.defaultVeggieCatalog,
                        onSearchQueryChange = viewModel::updateSearchQuery,
                        onAddItemToCart = { viewModel.addItemToCart(it) },
                        onSetCartItem = { item, qty, price -> viewModel.setCartItem(item, qty, price) },
                        onDecrementCartItem = { viewModel.decrementCartItem(it) },
                        onRemoveCartItem = { viewModel.removeCartItem(it) },
                        onClearCart = viewModel::clearCart,
                        onEditCartItemPrice = viewModel::editCartItemPrice,
                        onEditCartItemQuantity = viewModel::editCartItemQuantity,
                        onAddCustomItem = viewModel::addCustomItem,
                        onUpdatePreviousOutstanding = viewModel::updatePreviousOutstanding,
                        onUpdateCashReceived = viewModel::updateCashReceived,
                        onGenerateInvoice = {
                            if (uiState.cartItems.isEmpty()) {
                                Toast.makeText(context, "Please select at least one item", Toast.LENGTH_SHORT).show()
                            } else {
                                val invoice = viewModel.generateInvoice()
                                selectedInvoiceForView = invoice
                                currentScreen = AppScreen.INVOICE_DETAIL
                            }
                        },
                        onManageItems = {
                            currentScreen = AppScreen.MANAGE_ITEMS
                        },
                        onBack = { currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.CUSTOMERS }
                    )
                }
                AppScreen.INVOICE_DETAIL -> {
                    val activeInvoice = selectedInvoiceForView ?: uiState.currentInvoice
                    if (activeInvoice != null) {
                        InvoiceDetailScreen(
                            invoice = activeInvoice,
                            onBackToCheckout = { currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.CHECKOUT },
                            onHome = {
viewModel.resetInvoice()
selectedInvoiceForView = null
currentScreen = AppScreen.HOME
},

                            onEditInvoice = {
                                viewModel.loadInvoiceForEditing(activeInvoice)
                                selectedInvoiceForView = null
                                currentScreen = AppScreen.CHECKOUT
                            }
                        )
                    } else {
                        currentScreen = AppScreen.CHECKOUT
                    }
                }
                AppScreen.INVOICE_HISTORY -> {
                    InvoiceHistoryScreen(
                        invoices = uiState.invoiceHistory,
                        currencySymbol = uiState.currencySymbol,
onInvoiceClick = { invoice ->
                            selectedInvoiceForView = invoice
                            currentScreen = AppScreen.INVOICE_DETAIL
                        },
                        
                        onBack = { currentScreen = AppScreen.HOME }
                    )
                }
                AppScreen.MANAGE_ITEMS -> {
                    ManageItemsScreen(
                        items = uiState.inventoryItems,
                        currencySymbol = uiState.currencySymbol,
                        onAddItem = viewModel::addInventoryItem,
                        onUpdateItem = viewModel::updateInventoryItem,
                        onDeleteItem = viewModel::deleteInventoryItem,
                        onBack = { currentScreen = AppScreen.CHECKOUT }
                    )
                }
            }
            
            // Floating Bottom Bar Overlay
            if (currentScreen in listOf(AppScreen.HOME, AppScreen.CUSTOMERS)) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(bottom = 24.dp),
                    contentAlignment = Alignment.BottomCenter
                ) {
                    Surface(
                        shape = androidx.compose.foundation.shape.RoundedCornerShape(percent = 50),
                        color = MaterialTheme.colorScheme.surfaceVariant,
                        tonalElevation = 8.dp,
                        shadowElevation = 8.dp,
                        modifier = Modifier.padding(horizontal = 32.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                            horizontalArrangement = Arrangement.spacedBy(32.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            val isHome = currentScreen == AppScreen.HOME
                            Surface(
                                shape = androidx.compose.foundation.shape.RoundedCornerShape(percent = 50),
                                color = if (isHome) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent,
                                modifier = Modifier.clickable { currentScreen = AppScreen.HOME }
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Home, 
                                        contentDescription = "Home",
                                        tint = if (isHome) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    if (isHome) {
                                        Text(
                                            "Home", 
                                            fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.onSecondaryContainer
                                        )
                                    }
                                }
                            }
                            
                            val isCust = currentScreen == AppScreen.CUSTOMERS
                            Surface(
                                shape = androidx.compose.foundation.shape.RoundedCornerShape(percent = 50),
                                color = if (isCust) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent,
                                modifier = Modifier.clickable { currentScreen = AppScreen.CUSTOMERS }
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Person, 
                                        contentDescription = "Customers",
                                        tint = if (isCust) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    if (isCust) {
                                        Text(
                                            "Customers", 
                                            fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.onSecondaryContainer
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
