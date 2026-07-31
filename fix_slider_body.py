import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

pattern = r"// Real Quantity Picker.*?HorizontalDivider\(modifier = Modifier\.padding\(bottom = 16\.dp\)\)"

new_body = """// Real Quantity Picker
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
                
                SimpleWheelPicker(
                    value = currentValue,
                    range = range,
                    onValueChange = { newValue ->
                        qtyStr = format(newValue)
                    },
                    format = format
                )
                
                HorizontalDivider(modifier = Modifier.padding(bottom = 16.dp))"""

text = re.sub(pattern, new_body, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

