import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("androidx.compose.foundation.gestures.detectVerticalDragGestures", "detectVerticalDragGestures")
text = text.replace("androidx.compose.foundation.gestures.detectTapGestures", "detectTapGestures")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

