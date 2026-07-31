import re

with open('app/src/main/java/com/example/ui/screens/InvoiceHistoryScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("@Composable\nimport androidx.compose.runtime.*\nfun InvoiceHistoryScreen(", "@Composable\nfun InvoiceHistoryScreen(")
text = text.replace("import androidx.compose.runtime.Composable", "import androidx.compose.runtime.Composable\nimport androidx.compose.runtime.*")

with open('app/src/main/java/com/example/ui/screens/InvoiceHistoryScreen.kt', 'w') as f:
    f.write(text)

