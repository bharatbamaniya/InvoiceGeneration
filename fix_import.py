with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()
text = text.replace("import androidx.compose.ui.graphics.Color\\nimport androidx.compose.ui.graphics.graphicsLayer", "import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.graphicsLayer")
with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
