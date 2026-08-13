import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

text = text.replace(".androidx.compose.foundation.background(", ".background(")
text = text.replace("androidx.compose.foundation.layout.Box(", "Box(")
text = text.replace("androidx.compose.ui.graphics.Brush.verticalGradient", "androidx.compose.ui.graphics.Brush.verticalGradient")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)

