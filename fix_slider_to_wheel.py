import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

# Add SimpleWheelPicker outside CheckoutScreen
wheel_picker_code = """
@Composable
fun SimpleWheelPicker(
    value: Float,
    range: List<Float>,
    onValueChange: (Float) -> Unit,
    format: (Float) -> String
) {
    val currentIndex = range.indexOf(value).coerceAtLeast(0)
    var dragOffset by remember { mutableStateOf(0f) }
    val itemHeightPx = with(androidx.compose.ui.platform.LocalDensity.current) { 48.dp.toPx() }
    
    Box(
        modifier = Modifier
            .height(240.dp)
            .fillMaxWidth()
            .pointerInput(Unit) {
                androidx.compose.foundation.gestures.detectVerticalDragGestures(
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
"""

text = text.replace("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ItemConfigDialog(", wheel_picker_code + "\n@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ItemConfigDialog(")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

