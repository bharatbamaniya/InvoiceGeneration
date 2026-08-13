import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

text = text.replace("import androidx.compose.foundation.layout.Row", "import androidx.compose.foundation.layout.Row\nimport androidx.compose.foundation.background")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)

