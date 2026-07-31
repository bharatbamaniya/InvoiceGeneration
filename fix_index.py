import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

# Replace range.indexOf(value).coerceAtLeast(0)
# with finding the closest element
old_index = "val currentIndex = range.indexOf(value).coerceAtLeast(0)"
new_index = """val currentIndex = remember(value, range) { 
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
    }"""

text = text.replace(old_index, new_index)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
