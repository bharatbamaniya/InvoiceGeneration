import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

old_textfield = """                        OutlinedTextField(
                            value = qtyStr,
                            onValueChange = { 
                                qtyStr = it 
                                sliderValue = (it.toFloatOrNull() ?: 0f).coerceIn(0f, 100f)
                            },"""

new_textfield = """                        OutlinedTextField(
                            value = qtyStr,
                            onValueChange = { 
                                qtyStr = it 
                            },"""

text = text.replace(old_textfield, new_textfield)

# Also fix the import errors, e.g. `androidx.compose.foundation.gestures.detectVerticalDragGestures` is fully qualified in code but not available?
# Wait, let's just make sure it's correct.

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

