import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

# Replace Slider with SimpleWheelPicker
old_slider = """                Slider(
                    value = currentValue,
                    onValueChange = { newValue ->
                        // find closest value in range
                        val closest = range.minByOrNull { kotlin.math.abs(it - newValue) } ?: newValue
                        qtyStr = format(closest)
                    },
                    valueRange = range.first()..range.last(),
                    /* continuous */
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)
                )"""

new_wheel = """                SimpleWheelPicker(
                    value = currentValue,
                    range = range,
                    onValueChange = { newValue ->
                        qtyStr = format(newValue)
                    },
                    format = format
                )"""

text = text.replace(old_slider, new_wheel)

old_def = """@Composable
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
}"""

new_def = """@OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun SimpleWheelPicker(
    value: Float,
    range: List<Float>,
    onValueChange: (Float) -> Unit,
    format: (Float) -> String
) {
    val listState = androidx.compose.foundation.lazy.rememberLazyListState()
    
    // Find initial index
    val initialIndex = remember {
        var minDiff = Float.MAX_VALUE
        var closestIdx = 0
        for (i in range.indices) {
            val diff = kotlin.math.abs(range[i] - value)
            if (diff < minDiff) {
                minDiff = diff
                closestIdx = i
            }
        }
        closestIdx
    }
    
    LaunchedEffect(Unit) {
        listState.scrollToItem(initialIndex)
    }
    
    // Track center item
    val centerIndex by remember {
        derivedStateOf {
            val layoutInfo = listState.layoutInfo
            val visibleItemsInfo = layoutInfo.visibleItemsInfo
            if (visibleItemsInfo.isEmpty()) {
                -1
            } else {
                val viewportHeight = layoutInfo.viewportEndOffset - layoutInfo.viewportStartOffset
                val centerLine = layoutInfo.viewportStartOffset + viewportHeight / 2
                var closestItem = visibleItemsInfo.first()
                var minDistance = Int.MAX_VALUE
                
                for (item in visibleItemsInfo) {
                    val itemCenter = item.offset + item.size / 2
                    val distance = kotlin.math.abs(itemCenter - centerLine)
                    if (distance < minDistance) {
                        minDistance = distance
                        closestItem = item
                    }
                }
                closestItem.index
            }
        }
    }
    
    // Update value when dragging stops and center item is settled
    LaunchedEffect(listState.isScrollInProgress, centerIndex) {
        if (!listState.isScrollInProgress && centerIndex in range.indices) {
            onValueChange(range[centerIndex])
        }
    }

    Box(
        modifier = Modifier
            .height(240.dp)
            .fillMaxWidth(),
        contentAlignment = Alignment.Center
    ) {
        // Highlight selection area
        Surface(
            modifier = Modifier.fillMaxWidth(0.5f).height(48.dp),
            color = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
            shape = RoundedCornerShape(8.dp)
        ) {}
        
        androidx.compose.foundation.lazy.LazyColumn(
            state = listState,
            flingBehavior = androidx.compose.foundation.gestures.snapping.rememberSnapFlingBehavior(lazyListState = listState),
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(vertical = 96.dp) // (240 - 48) / 2
        ) {
            items(range.size) { index ->
                val isSelected = index == centerIndex
                val alpha = if (isSelected) 1f else 0.4f
                val fontSize = if (isSelected) 28.sp else 20.sp
                val fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(48.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = format(range[index]),
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = alpha),
                        fontSize = fontSize,
                        fontWeight = fontWeight
                    )
                }
            }
        }
    }
}"""

if old_def in text:
    text = text.replace(old_def, new_def)
else:
    print("WARNING: old_def not found")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

