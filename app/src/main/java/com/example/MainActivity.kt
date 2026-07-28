package com.example

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
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
        bottomBar = {
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
        }
    ) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
            when (currentScreen) {
                AppScreen.HOME -> {
                    HomeScreen(
                        state = uiState,
                        onSettingsClick = { currentScreen = AppScreen.SETTINGS },
                        onNewInvoice = {
                            viewModel.clearCart()
                            currentScreen = AppScreen.CUSTOMERS 
                        },
                        onViewInvoices = { currentScreen = AppScreen.INVOICE_HISTORY }
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
                            invoices = uiState.invoiceHistory.filter { it.customerId == customer.id },
                            payments = uiState.payments.filter { it.customerId == customer.id },
                            currencySymbol = uiState.currencySymbol,
                            onBack = { currentScreen = AppScreen.CUSTOMERS },
                            onNewInvoice = { 
                                viewModel.clearCart()
                                currentScreen = AppScreen.CHECKOUT 
                            },
                            onSettleBalance = { amount, remark -> viewModel.settleCustomerBalance(customer.id, amount, remark) },
                            onViewInvoice = { invoice ->
                                selectedInvoiceForView = invoice
                                currentScreen = AppScreen.INVOICE_DETAIL
                            }
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
                        }
                    )
                }
                AppScreen.INVOICE_DETAIL -> {
                    val activeInvoice = selectedInvoiceForView ?: uiState.currentInvoice
                    if (activeInvoice != null) {
                        InvoiceDetailScreen(
                            invoice = activeInvoice,
                            onBackToCheckout = { currentScreen = if (uiState.selectedCustomerId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.CHECKOUT },
                            onNewSale = {
                                val prevCustId = uiState.selectedCustomerId
                                viewModel.resetInvoice()
                                selectedInvoiceForView = null
                                viewModel.selectCustomer(prevCustId)
                                currentScreen = if (prevCustId != null) AppScreen.CUSTOMER_DETAIL else AppScreen.CHECKOUT
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
                        onSelectInvoice = { invoice ->
                            selectedInvoiceForView = invoice
                            currentScreen = AppScreen.INVOICE_DETAIL
                        },
                        onEditInvoice = { invoice ->
                            viewModel.loadInvoiceForEditing(invoice)
                            currentScreen = AppScreen.CHECKOUT
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
        }
    }
}
