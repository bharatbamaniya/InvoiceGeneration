import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

# Replace SimpleWheelPicker usage with Slider
old_usage = """                SimpleWheelPicker(
                    value = currentValue,
                    range = range,
                    onValueChange = { newValue ->
                        qtyStr = format(newValue)
                    },
                    format = format
                )"""

new_usage = """                Slider(
                    value = currentValue,
                    onValueChange = { newValue ->
                        // find closest value in range
                        val closest = range.minByOrNull { kotlin.math.abs(it - newValue) } ?: newValue
                        qtyStr = format(closest)
                    },
                    valueRange = range.first()..range.last(),
                    steps = range.size - 2, // -2 because steps are between min and max
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)
                )"""

text = text.replace(old_usage, new_usage)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

