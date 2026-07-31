import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

# fix state.previousOutstanding text field issue with string state
pattern = r"OutlinedTextField\(\s*value = state\.previousOutstanding\.toString\(\),\s*onValueChange = \{\s*onUpdatePreviousOutstanding\(it\.toDoubleOrNull\(\) \?\: 0\.0\)\s*\},"

new_field = """var prevOutStr by remember { mutableStateOf(if (state.previousOutstanding > 0) state.previousOutstanding.toString() else "") }
                    OutlinedTextField(
                        value = prevOutStr,
                        onValueChange = { 
                            prevOutStr = it
                            onUpdatePreviousOutstanding(it.toDoubleOrNull() ?: 0.0) 
                        },"""

text = re.sub(pattern, new_field, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
