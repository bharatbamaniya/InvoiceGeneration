package com.example.ui.components

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.snapping.rememberSnapFlingBehavior
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.example.model.GroceryItem
import java.util.Locale

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun WheelPicker(
    items: List<String>,
    initialIndex: Int,
    onItemSelected: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    val listState = rememberLazyListState(initialFirstVisibleItemIndex = maxOf(0, initialIndex))
    val flingBehavior = rememberSnapFlingBehavior(lazyListState = listState)
    val itemHeight = 48.dp

    LaunchedEffect(listState.isScrollInProgress) {
        if (!listState.isScrollInProgress) {
            val layoutInfo = listState.layoutInfo
            val centerOffset = (layoutInfo.viewportStartOffset + layoutInfo.viewportEndOffset) / 2
            var closestItem = -1
            var minDiff = Int.MAX_VALUE
            for (item in layoutInfo.visibleItemsInfo) {
                val itemCenter = item.offset + item.size / 2
                val diff = kotlin.math.abs(itemCenter - centerOffset)
                if (diff < minDiff) {
                    minDiff = diff
                    closestItem = item.index
                }
            }
            if (closestItem != -1) {
                // Accounting for the empty spacer at the top (index 0)
                if (closestItem >= 1 && closestItem <= items.size) {
                    onItemSelected(closestItem - 1)
                }
            }
        }
    }

    Box(
        modifier = modifier.height(itemHeight * 3),
        contentAlignment = Alignment.Center
    ) {
        // Selection highlight background
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(itemHeight)
                .clip(RoundedCornerShape(8.dp))
                .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.15f))
        )
        
        LazyColumn(
            state = listState,
            flingBehavior = flingBehavior,
            modifier = Modifier.fillMaxSize()
        ) {
            item { Spacer(modifier = Modifier.height(itemHeight)) }
            itemsIndexed(items) { index, item ->
                Box(
                    modifier = Modifier
                        .height(itemHeight)
                        .fillMaxWidth(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = item,
                        fontSize = 24.sp,
                        color = MaterialTheme.colorScheme.onSurface,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
            item { Spacer(modifier = Modifier.height(itemHeight)) }
        }
    }
}

@Composable
fun ItemConfigSheet(
    item: GroceryItem,
    initialQty: Double,
    initialPrice: Double,
    currencySymbol: String,
    onDismiss: () -> Unit,
    onConfirm: (qty: Double, price: Double) -> Unit
) {
    val isWeight = item.unit.lowercase(Locale.ROOT) == "kg"
    var selectedUnit by remember { 
        mutableStateOf(
            if (isWeight) {
                if (initialQty > 0.0 && initialQty < 1.0) "gm"
                else if (initialQty > 0.0 && (initialQty * 10).toInt() % 5 != 0) "gm"
                else "kg"
            } else item.unit
        ) 
    }
    
    var priceValue by remember { mutableStateOf(initialPrice) }
    var showEditPrice by remember { mutableStateOf(false) }
    var priceStr by remember { mutableStateOf(initialPrice.toString()) }

    // Pre-calculate items
    val kgItems = remember { (1..200).map { String.format(Locale.US, "%.1f", it * 0.5) } }
    val gmItems = remember { (1..100).map { (it * 50).toString() } }
    val pcItems = remember { (1..500).map { it.toString() } }

    var selectedKgIndex by remember { 
        mutableStateOf(kgItems.indexOf(String.format(Locale.US, "%.1f", if (initialQty > 0) initialQty else 1.0)).coerceAtLeast(0))
    }
    var selectedGmIndex by remember { 
        mutableStateOf(gmItems.indexOf((if (initialQty > 0) initialQty * 1000 else 50.0).toInt().toString()).coerceAtLeast(0))
    }
    var selectedPcIndex by remember { 
        mutableStateOf(pcItems.indexOf(if (initialQty > 0) initialQty.toInt().toString() else "1").coerceAtLeast(0))
    }

    Dialog(onDismissRequest = onDismiss) {
        Surface(
            shape = RoundedCornerShape(24.dp),
            color = MaterialTheme.colorScheme.surface,
            tonalElevation = 8.dp,
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "${item.iconEmoji} ${item.name}",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    textAlign = TextAlign.Center
                )
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Unit Selector
                if (isWeight) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Center
                    ) {
                        SegmentedButton(
                            text = "kg",
                            isSelected = selectedUnit == "kg",
                            onClick = { selectedUnit = "kg" }
                        )
                        Spacer(modifier = Modifier.width(12.dp))
                        SegmentedButton(
                            text = "gm",
                            isSelected = selectedUnit == "gm",
                            onClick = { selectedUnit = "gm" }
                        )
                    }
                    Spacer(modifier = Modifier.height(24.dp))
                }
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Center
                ) {
                    Box(modifier = Modifier.width(120.dp)) {
                        if (selectedUnit == "kg") {
                            WheelPicker(items = kgItems, initialIndex = selectedKgIndex, onItemSelected = { selectedKgIndex = it })
                        } else if (selectedUnit == "gm") {
                            WheelPicker(items = gmItems, initialIndex = selectedGmIndex, onItemSelected = { selectedGmIndex = it })
                        } else {
                            WheelPicker(items = pcItems, initialIndex = selectedPcIndex, onItemSelected = { selectedPcIndex = it })
                        }
                    }
                    
                    Spacer(modifier = Modifier.width(16.dp))
                    
                    Text(
                        text = selectedUnit,
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Medium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                Spacer(modifier = Modifier.height(32.dp))
                
                // Price Section (Compact)
                if (showEditPrice) {
                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = { 
                            priceStr = it
                            it.toDoubleOrNull()?.let { p -> priceValue = p }
                        },
                        label = { Text("Price ($currencySymbol)") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                        modifier = Modifier.fillMaxWidth()
                    )
                } else {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .clickable { showEditPrice = true }
                            .padding(8.dp)
                    ) {
                        Text(
                            text = "Price: $currencySymbol$priceValue",
                            fontSize = 16.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Icon(
                            Icons.Default.Edit, 
                            contentDescription = "Edit Price", 
                            modifier = Modifier.size(16.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = onDismiss) {
                        Text("Cancel")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    Button(
                        onClick = {
                            val finalQty = when(selectedUnit) {
                                "kg" -> kgItems[selectedKgIndex].toDouble()
                                "gm" -> gmItems[selectedGmIndex].toDouble() / 1000.0
                                else -> pcItems[selectedPcIndex].toDouble()
                            }
                            onConfirm(finalQty, priceValue)
                        }
                    ) {
                        Text("Confirm")
                    }
                }
            }
        }
    }
}

@Composable
fun SegmentedButton(text: String, isSelected: Boolean, onClick: () -> Unit) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
        contentColor = if (isSelected) Color.White else MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = Modifier.clickable { onClick() }
    ) {
        Text(
            text = text,
            modifier = Modifier.padding(horizontal = 24.dp, vertical = 10.dp),
            fontWeight = FontWeight.Bold
        )
    }
}
