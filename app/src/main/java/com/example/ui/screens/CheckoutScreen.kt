package com.example.ui.screens

import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.foundation.text.KeyboardOptions
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.isImeVisible
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.ime
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Inventory
import androidx.compose.material.icons.filled.Receipt
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.model.GroceryItem
import com.example.model.Invoice
import com.example.ui.components.AddCustomItemDialog
import com.example.ui.components.ItemChipCard
import com.example.ui.components.ItemConfigSheet
import com.example.viewmodel.InvoiceUiState
import java.util.Locale




@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun CheckoutScreen(
    state: InvoiceUiState,
    defaultItems: List<GroceryItem>,
    onSearchQueryChange: (String) -> Unit,
    onAddItemToCart: (GroceryItem) -> Unit,
    onSetCartItem: (GroceryItem, Double, Double) -> Unit,
    onDecrementCartItem: (String) -> Unit,
    onRemoveCartItem: (String) -> Unit,
    onClearCart: () -> Unit,
    onEditCartItemPrice: (String, Double) -> Unit,
    onEditCartItemQuantity: (String, Double) -> Unit,
    onAddCustomItem: (name: String, price: Double, unit: String) -> Unit,
    onUpdatePreviousOutstanding: (Double) -> Unit,
    onUpdateCashReceived: (Double) -> Unit,
    onGenerateInvoice: () -> Unit,
    onManageItems: () -> Unit
) {
    val context = LocalContext.current
    var showCustomItemDialog by remember { mutableStateOf(false) }
    var showCheckoutSheet by remember { mutableStateOf(false) }
    var selectedItemForConfig by remember { mutableStateOf<GroceryItem?>(null) }
    var isSearchFocused by remember { mutableStateOf(false) }

    // All available items
    val allAvailableItems = state.inventoryItems
    val filteredItems = if (state.searchQuery.isEmpty()) {
        allAvailableItems
    } else {
        allAvailableItems.filter { it.name.contains(state.searchQuery, ignoreCase = true) }
    }
    
    val subtotalAmount = state.cartItems.sumOf { (it.customPrice ?: it.item.price) * it.quantity }
    val totalCartCount = state.cartItems.sumOf { it.quantity }
    val totalCartCountStr = if (totalCartCount % 1.0 == 0.0) totalCartCount.toInt().toString() else String.format(Locale.US, "%.2f", totalCartCount)
    
    val totalBalance = subtotalAmount




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
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 16.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {

            // Search Bar & Add Custom Item Action
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Surface(
                    shape = RoundedCornerShape(percent = 50),
                    shadowElevation = 4.dp,
                    color = MaterialTheme.colorScheme.surface,
                    modifier = Modifier.weight(1f)
                ) {
                    androidx.compose.material3.TextField(
                        value = state.searchQuery,
                        onValueChange = onSearchQueryChange,
                        placeholder = { Text("Search items...", style = MaterialTheme.typography.bodyMedium) },
                        leadingIcon = { Icon(Icons.Default.Search, contentDescription = null, modifier = Modifier.size(20.dp)) },
                        trailingIcon = {
                            if (state.searchQuery.isNotEmpty()) {
                                IconButton(onClick = { onSearchQueryChange("") }, modifier = Modifier.size(24.dp)) {
                                    Icon(Icons.Default.Clear, contentDescription = "Clear", modifier = Modifier.size(16.dp))
                                }
                            }
                        },
                        singleLine = true,
                        textStyle = MaterialTheme.typography.bodyMedium,
                        colors = androidx.compose.material3.TextFieldDefaults.colors(
                            focusedContainerColor = Color.Transparent,
                            unfocusedContainerColor = Color.Transparent,
                            focusedIndicatorColor = Color.Transparent,
                            unfocusedIndicatorColor = Color.Transparent,
                            disabledIndicatorColor = Color.Transparent
                        ),
                        modifier = Modifier
                            .height(54.dp)
                            .onFocusChanged { isSearchFocused = it.isFocused }
                            .testTag("item_search_input")
                    )
                }

                Button(
                    onClick = { showCustomItemDialog = true },
                    shape = RoundedCornerShape(12.dp),
                    contentPadding = PaddingValues(horizontal = 12.dp),
                    modifier = Modifier
                        .height(50.dp)
                        .testTag("add_custom_item_dialog_button")
                ) {
                    Icon(Icons.Default.Add, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("Add Item", fontSize = 13.sp)
                }
            }

            // Grocery Items Grid
            Text(
                text = "TAP TO ADD TO INVOICE (${filteredItems.size})",
                style = MaterialTheme.typography.labelSmall,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
                modifier = Modifier.weight(1f)
            ) {
                items(filteredItems, key = { it.id }) { item ->
                    val cartItem = state.cartItems.find { it.item.id == item.id }
                    val qtyInCart = cartItem?.quantity ?: 0.0

                    ItemChipCard(
                        item = item,
                        quantityInCart = qtyInCart,
                        currencySymbol = state.currencySymbol,
                        onClick = { selectedItemForConfig = item }
                    )
                }
            }
        }
    }

    // Dialogs
    if (showCustomItemDialog) {
        AddCustomItemDialog(
            currencySymbol = state.currencySymbol,
            onDismiss = { showCustomItemDialog = false },
            onAddItem = { name, price, unit ->
                onAddCustomItem(name, price, unit)
            }
        )
    }



    selectedItemForConfig?.let { item ->
        val cartItem = state.cartItems.find { it.item.id == item.id }
        ItemConfigSheet(
            item = item,
            initialQty = cartItem?.quantity ?: 0.0,
            initialPrice = cartItem?.customPrice ?: item.price,
            currencySymbol = state.currencySymbol,
            onDismiss = { selectedItemForConfig = null },
            onConfirm = { qty, price ->
                if (qty > 0) {
                    onSetCartItem(item, qty, price)
                } else {
                    onRemoveCartItem(item.id)
                }
                selectedItemForConfig = null
            }
        )
    }

    if (showCheckoutSheet) {
        var showItems by remember { androidx.compose.runtime.mutableStateOf(false) }
        androidx.compose.material3.ModalBottomSheet(
            onDismissRequest = { showCheckoutSheet = false }
        ) {
            LazyColumn(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                item {
                    Text(text = "Checkout Summary", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                }

                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "$totalCartCountStr items selected",
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.padding(4.dp)
                        )

                        TextButton(onClick = {
                            onClearCart()
                            showCheckoutSheet = false
                        }) {
                            Icon(
                                imageVector = Icons.Default.Delete,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp)
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("Clear All")
                        }
                    }
                }

                if (state.cartItems.isNotEmpty()) {
                    item {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { showItems = !showItems }
                                .padding(vertical = 8.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "View/Edit Items (${state.cartItems.size})",
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Medium,
                                color = MaterialTheme.colorScheme.primary
                            )
                            Icon(
                                imageVector = if (showItems) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                                contentDescription = "Toggle Items",
                                tint = MaterialTheme.colorScheme.primary
                            )
                        }
                    }

                    if (showItems) {
                        items(state.cartItems) { invoiceItem ->
                            var priceStr by remember(invoiceItem.item.id, invoiceItem.customPrice) { 
                                androidx.compose.runtime.mutableStateOf(invoiceItem.unitPrice.toString()) 
                            }
                            var qtyStr by remember(invoiceItem.item.id, invoiceItem.quantity) {
                                val qtyVal = invoiceItem.quantity
                                val str = if (qtyVal % 1.0 == 0.0) qtyVal.toInt().toString() else qtyVal.toString()
                                androidx.compose.runtime.mutableStateOf(str)
                            }
                            
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "${invoiceItem.item.iconEmoji} ${invoiceItem.item.name}",
                                    style = MaterialTheme.typography.bodyMedium,
                                    fontWeight = FontWeight.Medium,
                                    modifier = Modifier.weight(1.5f)
                                )
                                
                                OutlinedTextField(
                                    value = qtyStr,
                                    onValueChange = { newVal ->
                                        qtyStr = newVal
                                        newVal.toDoubleOrNull()?.let {
                                            if(it > 0) onEditCartItemQuantity(invoiceItem.item.id, it)
                                        }
                                    },
                                    label = { Text("Qty", fontSize = 11.sp) },
                                    singleLine = true,
                                    textStyle = androidx.compose.ui.text.TextStyle(fontSize = 13.sp),
                                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                                    modifier = Modifier.weight(1f).padding(end = 4.dp)
                                )
                                OutlinedTextField(
                                    value = priceStr,
                                    onValueChange = { newVal ->
                                        priceStr = newVal
                                        newVal.toDoubleOrNull()?.let {
                                            onEditCartItemPrice(invoiceItem.item.id, it)
                                        }
                                    },
                                    label = { Text(state.currencySymbol, fontSize = 11.sp) },
                                    singleLine = true,
                                    textStyle = androidx.compose.ui.text.TextStyle(fontSize = 13.sp),
                                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                                    modifier = Modifier.weight(1f)
                                )
                                IconButton(
                                    onClick = { onRemoveCartItem(invoiceItem.item.id) },
                                    modifier = Modifier.size(32.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Delete,
                                        contentDescription = "Remove",
                                        tint = MaterialTheme.colorScheme.error,
                                        modifier = Modifier.size(18.dp)
                                    )
                                }
                            }
                        }
                    }
                }

                item {
                    var showAdvancedPayment by remember { androidx.compose.runtime.mutableStateOf(false) }

                    Column(modifier = Modifier.fillMaxWidth()) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { showAdvancedPayment = !showAdvancedPayment }
                                .padding(vertical = 12.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(
                                    text = "Bill Amount:",
                                    style = MaterialTheme.typography.bodyLarge
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(
                                    imageVector = if (showAdvancedPayment) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                                    contentDescription = "Toggle Advanced Payment",
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                            Text(
                                text = String.format(Locale.US, "%s%.2f", state.currencySymbol, subtotalAmount),
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.Medium
                            )
                        }

                        if (showAdvancedPayment) {
                            Row(
                                horizontalArrangement = Arrangement.spacedBy(16.dp),
                                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp)
                            ) {
                                OutlinedTextField(
                                    value = if (state.previousOutstanding == 0.0) "" else state.previousOutstanding.toString(),
                                    onValueChange = { onUpdatePreviousOutstanding(it.toDoubleOrNull() ?: 0.0) },
                                    label = { Text("Prev Outstanding", fontSize = 13.sp) },
                                    singleLine = true,
                                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                                    modifier = Modifier.weight(1f)
                                )
                                OutlinedTextField(
                                    value = if (state.cashReceived == 0.0) "" else state.cashReceived.toString(),
                                    onValueChange = { onUpdateCashReceived(it.toDoubleOrNull() ?: 0.0) },
                                    label = { Text("Cash Received", fontSize = 13.sp) },
                                    singleLine = true,
                                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                                    modifier = Modifier.weight(1f)
                                )
                            }
                        }
                    }
                }

                item {
                    Button(
                        onClick = {
                            onGenerateInvoice()
                            showCheckoutSheet = false
                        },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Color(0xFF1B5E20)
                        ),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(54.dp)
                            .testTag("generate_invoice_button")
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "GENERATE INVOICE",
                                fontWeight = FontWeight.Bold,
                                fontSize = 16.sp,
                                color = Color.White
                            )
                            Text(
                                text = String.format(Locale.US, "%s%.2f ➔", state.currencySymbol, totalBalance),
                                fontWeight = FontWeight.ExtraBold,
                                fontSize = 18.sp,
                                color = Color.White
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                }
            }
        }
    }
}
