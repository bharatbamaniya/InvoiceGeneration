with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("import detectVerticalDragGestures", "import androidx.compose.foundation.gestures.detectVerticalDragGestures")
text = text.replace("import detectTapGestures", "import androidx.compose.foundation.gestures.detectTapGestures")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
