import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

text = text.replace(".androidx.compose.ui.graphics.graphicsLayer { rotationZ = -90f }", ".graphicsLayer { rotationZ = -90f }")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

