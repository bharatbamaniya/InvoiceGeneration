package com.example.ui.screens

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale
import androidx.compose.foundation.background
import androidx.compose.ui.draw.clip

import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.model.GroceryItem
import com.example.viewmodel.InvoiceUiState
import java.util.Locale
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.IntSize


@OptIn(ExperimentalMaterial3Api::class)
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
    onManageItems: () -> Unit,
    onBack: () -> Unit
) {
    val context = LocalContext.current
    var showCheckoutSheet by remember { mutableStateOf(false) }
    var selectedItemForConfig by remember { mutableStateOf<GroceryItem?>(null) }
    var showCustomItemDialog by remember { mutableStateOf(false) }
    
    val allAvailableItems = state.inventoryItems
    val filteredItems = if (state.searchQuery.isEmpty()) {
        allAvailableItems
    } else {
        allAvailableItems.filter { it.name.contains(state.searchQuery, ignoreCase = true) }
    }
    
    val cartTotal = state.cartItems.sumOf { it.totalPrice }
    val cartItemCount = state.cartItems.size

    val customerName = state.customers.find { it.id == state.selectedCustomerId }?.name ?: "New Invoice"

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Column {
                        Text(customerName, fontWeight = FontWeight.Bold)
                        Text("New invoice", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                    titleContentColor = MaterialTheme.colorScheme.onBackground
                )
            )
        },
        floatingActionButton = {
            if (cartItemCount > 0) {
                ExtendedFloatingActionButton(
                    onClick = { showCheckoutSheet = true },
                    modifier = Modifier.padding(bottom = 16.dp),
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary,
                    shape = RoundedCornerShape(28.dp),
                    icon = { Icon(Icons.Default.ShoppingCart, contentDescription = "Checkout") },
                    text = { 
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("Checkout", fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.width(8.dp))
                            Surface(
                                color = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.2f),
                                shape = RoundedCornerShape(16.dp)
                            ) {
                                Text(
                                    "${state.currencySymbol}${String.format(Locale.US, "%.2f", cartTotal)}",
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                )
            }
        },
        floatingActionButtonPosition = FabPosition.Center
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            
            // Search and Add
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                OutlinedTextField(
                    value = state.searchQuery,
                    onValueChange = onSearchQueryChange,
                    modifier = Modifier.weight(1f),
                    placeholder = { Text("Search items...") },
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search") },
                    shape = RoundedCornerShape(24.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        focusedBorderColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f),
                        unfocusedBorderColor = Color.Transparent
                    )
                )
                
                Surface(
                    onClick = { showCustomItemDialog = true },
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                    shape = RoundedCornerShape(24.dp),
                    modifier = Modifier.height(56.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Default.Add, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Add Item", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                    }
                }
            }
            
            Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(
                    "TAP TO ADD TO INVOICE (${allAvailableItems.size})",
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                TextButton(onClick = onManageItems) {
                    Text("Manage Catalog")
                }
            }

            
            // Grid
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                contentPadding = PaddingValues(start = 16.dp, end = 16.dp, bottom = 100.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(filteredItems) { item ->
                    val cartItem = state.cartItems.find { it.item.id == item.id }
                    val isSelected = cartItem != null && cartItem.quantity > 0
                    
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { selectedItemForConfig = item },
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = if (isSelected) 0.1f else 0.3f)
                        ),
                        border = if (isSelected) androidx.compose.foundation.BorderStroke(2.dp, MaterialTheme.colorScheme.primary) else null
                    ) {
                        Row(
                            modifier = Modifier.padding(12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Surface(
                                shape = RoundedCornerShape(percent = 50),
                                color = MaterialTheme.colorScheme.surfaceVariant,
                                modifier = Modifier.size(32.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    if (item.iconEmoji.startsWith("content://") || item.iconEmoji.startsWith("http")) {
                                        AsyncImage(
                                            model = item.iconEmoji,
                                            contentDescription = item.name,
                                            contentScale = ContentScale.Crop,
                                            modifier = Modifier.fillMaxSize()
                                        )
                                    } else {
                                        Text(
                                            item.name.take(1).uppercase(), 
                                            fontWeight = FontWeight.Bold,
                                            style = MaterialTheme.typography.labelLarge,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }
                                }
                            }
                            
                            Spacer(modifier = Modifier.width(8.dp))
                            
                            Column(modifier = Modifier.weight(1f)) {
                                Text(item.name, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.bodyMedium, maxLines = 1)
                                Text("${state.currencySymbol}${String.format(Locale.US, "%.0f", item.price)}/${item.unit}", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            
                            if (isSelected) {
                                Surface(
                                    color = MaterialTheme.colorScheme.primary,
                                    shape = RoundedCornerShape(8.dp)
                                ) {
                                    Text(
                                        String.format(Locale.US, "%.1f", cartItem!!.quantity),
                                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                                        style = MaterialTheme.typography.labelSmall,
                                        fontWeight = FontWeight.Bold,
                                        color = MaterialTheme.colorScheme.onPrimary
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
        

        if (showCustomItemDialog) {
            CustomItemDialog(
                currencySymbol = state.currencySymbol,
                onDismiss = { showCustomItemDialog = false },
                onConfirm = { name, price, unit ->
                    onAddCustomItem(name, price, unit)
                    showCustomItemDialog = false
                }
            )
        }
        if (selectedItemForConfig != null) {
            val item = selectedItemForConfig!!
            val cartItem = state.cartItems.find { it.item.id == item.id }
            
            ItemConfigDialog(
                item = item,
                initialQuantity = cartItem?.quantity ?: 0.0,
                initialPrice = cartItem?.customPrice ?: item.price,
                currencySymbol = state.currencySymbol,
                onDismiss = { selectedItemForConfig = null },
                onConfirm = { qty, price ->
                    onSetCartItem(item, qty, price)
                    selectedItemForConfig = null
                }
            )
        }
        
        if (showCheckoutSheet) {
            CheckoutSummarySheet(
                state = state,
                onDismiss = { showCheckoutSheet = false },
                onGenerateInvoice = {
                    onGenerateInvoice()
                    showCheckoutSheet = false
                },
                onClearCart = {
                    onClearCart()
                    showCheckoutSheet = false
                },
                onRemoveItem = onRemoveCartItem,
                onUpdateQty = onEditCartItemQuantity,
                onUpdatePrice = onEditCartItemPrice,
                onUpdateCash = onUpdateCashReceived,
                onUpdatePreviousOutstanding = onUpdatePreviousOutstanding
            )
        }
    }
}


@Composable
fun SimpleWheelPicker(
    value: Float,
    range: List<Float>,
    onValueChange: (Float) -> Unit,
    format: (Float) -> String
) {
    val currentIndex = remember(value, range) { 
        var closestIdx = 0
        var minDiff = Float.MAX_VALUE
        for (i in range.indices) {
            val diff = kotlin.math.abs(range[i] - value)
            if (diff < minDiff) {
                minDiff = diff
                closestIdx = i
            }
        }
        closestIdx
    }
    var dragOffset by remember { mutableStateOf(0f) }
    val itemHeightPx = with(androidx.compose.ui.platform.LocalDensity.current) { 48.dp.toPx() }
    
    Box(
        modifier = Modifier
            .height(240.dp)
            .fillMaxWidth()
            .pointerInput(Unit) {
                detectVerticalDragGestures(
                    onDragEnd = { dragOffset = 0f },
                    onDragCancel = { dragOffset = 0f }
                ) { change, dragAmount ->
                    change.consume()
                    dragOffset += dragAmount
                    if (kotlin.math.abs(dragOffset) > itemHeightPx) {
                        val steps = (dragOffset / itemHeightPx).toInt()
                        dragOffset -= steps * itemHeightPx
                        val newIndex = (currentIndex - steps).coerceIn(0, range.size - 1)
                        if (newIndex != currentIndex) {
                            onValueChange(range[newIndex])
                        }
                    }
                }
            },
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            for (offset in -2..2) {
                val index = currentIndex + offset
                if (index in range.indices) {
                    val alpha = 1f - (kotlin.math.abs(offset) * 0.3f)
                    val fontSize = if (offset == 0) 32.sp else 24.sp
                    val fontWeight = if (offset == 0) FontWeight.Bold else FontWeight.Normal
                    Text(
                        text = format(range[index]),
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = alpha),
                        fontSize = fontSize,
                        fontWeight = fontWeight,
                        modifier = Modifier.height(48.dp).wrapContentHeight()
                    )
                } else {
                    Spacer(modifier = Modifier.height(48.dp))
                }
            }
        }
        
        Surface(
            modifier = Modifier.fillMaxWidth(0.5f).height(48.dp),
            color = MaterialTheme.colorScheme.primary.copy(alpha = 0.1f),
            shape = RoundedCornerShape(8.dp)
        ) {}
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ItemConfigDialog(
    item: GroceryItem,
    initialQuantity: Double,
    initialPrice: Double,
    currencySymbol: String,
    onDismiss: () -> Unit,
    onConfirm: (Double, Double) -> Unit
) {
    var qtyStr by remember { mutableStateOf(if (initialQuantity > 0) initialQuantity.toString() else "1.0") }
    var priceStr by remember { mutableStateOf(initialPrice.toString()) }
    
    // Quick unit toggle (kg/gm) simulation
    var isGm by remember { mutableStateOf(false) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { 
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center, modifier = Modifier.fillMaxWidth()) {
                Surface(
                    shape = RoundedCornerShape(percent = 50),
                    color = MaterialTheme.colorScheme.surfaceVariant,
                    modifier = Modifier.size(32.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        if (item.iconEmoji.startsWith("content://") || item.iconEmoji.startsWith("http")) {
                            AsyncImage(
                                model = item.iconEmoji,
                                contentDescription = item.name,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier.fillMaxSize()
                            )
                        } else {
                            Text(item.name.take(1).uppercase(), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
                Spacer(modifier = Modifier.width(8.dp))
                Text(item.name, fontWeight = FontWeight.Bold, fontSize = 20.sp)
            }
        },
        text = {
            Column(
                modifier = Modifier.fillMaxWidth(),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                
                                // Unit toggle
                if (item.unit == "kg") {
                    Row(
                        modifier = Modifier.padding(bottom = 24.dp).background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(24.dp))
                    ) {
                        Surface(
                            color = if (!isGm) MaterialTheme.colorScheme.primary else Color.Transparent,
                            shape = RoundedCornerShape(24.dp),
                            modifier = Modifier.clickable { 
                                if (isGm) {
                                    isGm = false
                                    val currentGm = qtyStr.toFloatOrNull() ?: 0f
                                    qtyStr = String.format(java.util.Locale.US, "%.1f", currentGm / 1000f)
                                }
                            }
                        ) {
                            Text("kg", modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp), color = if (!isGm) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                        Surface(
                            color = if (isGm) MaterialTheme.colorScheme.primary else Color.Transparent,
                            shape = RoundedCornerShape(24.dp),
                            modifier = Modifier.clickable { 
                                if (!isGm) {
                                    isGm = true
                                    val currentKg = qtyStr.toFloatOrNull() ?: 0f
                                    qtyStr = (currentKg * 1000f).toInt().toString()
                                }
                            }
                        ) {
                            Text("gm", modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp), color = if (isGm) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                    }
                }
                
                                // Real Quantity Picker
                val (range, format) = remember(item.unit, isGm) {
                    when {
                        item.unit == "kg" && isGm -> {
                            val r = generateSequence(0f) { it + 50f }.takeWhile { it <= 5000f }.toList()
                            val f: (Float) -> String = { it.toInt().toString() }
                            r to f
                        }
                        item.unit == "kg" && !isGm -> {
                            val r = generateSequence(0f) { it + 0.5f }.takeWhile { it <= 500f }.toList()
                            val f: (Float) -> String = { if (it % 1.0 < 0.1 || it % 1.0 > 0.9) it.toInt().toString() else String.format(java.util.Locale.US, "%.1f", it) }
                            r to f
                        }
                        else -> {
                            val r = generateSequence(0f) { it + 1f }.takeWhile { it <= 40f }.toList()
                            val f: (Float) -> String = { it.toInt().toString() }
                            r to f
                        }
                    }
                }
                
                val currentValue = qtyStr.toFloatOrNull() ?: 0f
                
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 16.dp)) {
                    Text(
                        text = qtyStr,
                        style = MaterialTheme.typography.displayLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary,
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = if (isGm && item.unit == "kg") "gm" else item.unit,
                        style = MaterialTheme.typography.titleLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                SimpleWheelPicker(
                    value = currentValue,
                    range = range,
                    onValueChange = { newValue ->
                        qtyStr = format(newValue)
                    },
                    format = format
                )
                
                HorizontalDivider(modifier = Modifier.padding(bottom = 16.dp))

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Price: $currencySymbol", style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold)
                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = { priceStr = it },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.width(80.dp).height(48.dp),
                        textStyle = LocalTextStyle.current.copy(fontWeight = FontWeight.Bold),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Color.Transparent,
                            unfocusedBorderColor = Color.Transparent,
                            focusedContainerColor = Color.Transparent,
                            unfocusedContainerColor = Color.Transparent
                        )
                    )
                    Icon(Icons.Default.Edit, contentDescription = "Edit", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    var qty = qtyStr.toDoubleOrNull() ?: 0.0
                    val price = priceStr.toDoubleOrNull() ?: item.price
                    if (isGm && item.unit == "kg") {
                        qty /= 1000.0
                    }
                    onConfirm(qty, price)
                },
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
            ) {
                Text("Confirm")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        },
        containerColor = MaterialTheme.colorScheme.surface,
        shape = RoundedCornerShape(24.dp)
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CheckoutSummarySheet(
    state: InvoiceUiState,
    onDismiss: () -> Unit,
    onGenerateInvoice: () -> Unit,
    onClearCart: () -> Unit,
    onRemoveItem: (String) -> Unit,
    onUpdateQty: (String, Double) -> Unit,
    onUpdatePrice: (String, Double) -> Unit,
    onUpdateCash: (Double) -> Unit,
    onUpdatePreviousOutstanding: (Double) -> Unit
) {
    var itemsExpanded by remember { mutableStateOf(false) }
    var billExpanded by remember { mutableStateOf(false) }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = MaterialTheme.colorScheme.background,
        dragHandle = { BottomSheetDefaults.DragHandle() }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 8.dp)
                .padding(bottom = 32.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Checkout Summary", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                TextButton(onClick = onClearCart) {
                    Icon(Icons.Default.Delete, contentDescription = "Clear All", modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("Clear All")
                }
            }
            
            Text("${state.cartItems.size} items selected", color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(bottom = 16.dp))
            
            Row(modifier = Modifier.fillMaxWidth().clickable { itemsExpanded = !itemsExpanded }.padding(vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("View/Edit Items (${state.cartItems.size})", fontWeight = FontWeight.Bold)
                Icon(if (itemsExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            
            if (itemsExpanded) {
                Spacer(modifier = Modifier.height(16.dp))
                
                // Items List
                Column(
                    modifier = Modifier.heightIn(max = 240.dp).fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    state.cartItems.forEach { cartItem ->
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Surface(
                                shape = RoundedCornerShape(percent = 50),
                                color = MaterialTheme.colorScheme.surfaceVariant,
                                modifier = Modifier.size(32.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    if (cartItem.item.iconEmoji.startsWith("content://") || cartItem.item.iconEmoji.startsWith("http")) {
                                        AsyncImage(
                                            model = cartItem.item.iconEmoji,
                                            contentDescription = cartItem.item.name,
                                            contentScale = ContentScale.Crop,
                                            modifier = Modifier.fillMaxSize()
                                        )
                                    } else {
                                        Text(cartItem.item.name.take(1).uppercase(), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    }
                                }
                            }
                            
                            Spacer(modifier = Modifier.width(8.dp))
                            
                            Column(modifier = Modifier.weight(1f)) {
                                Text(cartItem.item.name, fontWeight = FontWeight.Bold, maxLines = 1)
                                val qtyFormat = if (cartItem.quantity % 1.0 == 0.0) cartItem.quantity.toInt().toString() else cartItem.quantity.toString()
                                val price = cartItem.customPrice ?: cartItem.item.price
                                val priceFormat = if (price % 1.0 == 0.0) price.toInt().toString() else price.toString()
                                Text("$qtyFormat ${cartItem.item.unit} x ${state.currencySymbol ?: "$"}$priceFormat", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            
                            val itemTotal = cartItem.quantity * (cartItem.customPrice ?: cartItem.item.price)
                            val totalFormat = if (itemTotal % 1.0 == 0.0) itemTotal.toInt().toString() else String.format(java.util.Locale.US, "%.2f", itemTotal)
                            Text("${state.currencySymbol ?: "$"}$totalFormat", fontWeight = FontWeight.Bold)
                            
                            Spacer(modifier = Modifier.width(16.dp))
                            
                            IconButton(onClick = { onRemoveItem(cartItem.item.id) }, modifier = Modifier.size(24.dp)) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove", tint = MaterialTheme.colorScheme.error)
                            }
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            HorizontalDivider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth().clickable { billExpanded = !billExpanded }.padding(vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Bill Amount:", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.width(8.dp))
                    Icon(if (billExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                Text("${state.currencySymbol}${String.format(Locale.US, "%.2f", state.cartItems.sumOf { it.totalPrice })}", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            }
            
            if (billExpanded) {
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    var prevOutStr by remember { mutableStateOf(if (state.previousOutstanding > 0) state.previousOutstanding.toString() else "") }
                    OutlinedTextField(
                        value = prevOutStr,
                        onValueChange = { 
                            prevOutStr = it
                            onUpdatePreviousOutstanding(it.toDoubleOrNull() ?: 0.0) 
                        },
                        label = { Text("Prev Outstanding", fontSize = 10.sp) },
                        modifier = Modifier.weight(1f),
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                            unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        )
                    )
                    
                    var cashStr by remember { mutableStateOf("") }
                    OutlinedTextField(
                        value = cashStr,
                        onValueChange = { 
                            cashStr = it
                            onUpdateCash(it.toDoubleOrNull() ?: 0.0) 
                        },
                        label = { Text("Cash Received", fontSize = 10.sp) },
                        modifier = Modifier.weight(1f),
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                            unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        )
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Button(
                onClick = onGenerateInvoice,
                modifier = Modifier.fillMaxWidth().height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50)), // Green color as per screenshot
                shape = RoundedCornerShape(28.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("GENERATE INVOICE", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            "${state.currencySymbol}${String.format(Locale.US, "%.2f", state.cartItems.sumOf { it.totalPrice } + state.previousOutstanding)}",
                            fontWeight = FontWeight.Bold,
                            fontSize = 16.sp
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = null, modifier = Modifier.size(18.dp)) // Assuming forward arrow
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CustomItemDialog(
    currencySymbol: String,
    onDismiss: () -> Unit,
    onConfirm: (String, Double, String) -> Unit
) {
    var name by remember { mutableStateOf("") }
    var priceStr by remember { mutableStateOf("") }
    var unit by remember { mutableStateOf("kg") }
    val units = listOf("kg", "gm", "pc", "bunch")
    var expanded by remember { mutableStateOf(false) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add Custom Item") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Item Name") },
                    modifier = Modifier.fillMaxWidth()
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = { priceStr = it },
                        label = { Text("Price ($currencySymbol)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f)
                    )
                    ExposedDropdownMenuBox(
                        expanded = expanded,
                        onExpandedChange = { expanded = !expanded },
                        modifier = Modifier.weight(1f)
                    ) {
                        OutlinedTextField(
                            value = unit,
                            onValueChange = {},
                            readOnly = true,
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                            modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth(),
                            label = { Text("Unit") }
                        )
                        ExposedDropdownMenu(
                            expanded = expanded,
                            onDismissRequest = { expanded = false },
                            modifier = Modifier
                        ) {
                            units.forEach { option ->
                                DropdownMenuItem(
                                    text = { Text(option) },
                                    onClick = {
                                        unit = option
                                        expanded = false
                                    }
                                )
                            }
                        }
                    }
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val price = priceStr.toDoubleOrNull() ?: 0.0
                    if (name.isNotBlank() && price > 0) {
                        onConfirm(name, price, unit)
                    }
                }
            ) {
                Text("Add")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
