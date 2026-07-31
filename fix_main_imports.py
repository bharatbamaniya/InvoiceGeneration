with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

imports_to_add = """
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Alignment
import androidx.compose.ui.draw.clip
"""

code = code.replace("import androidx.compose.foundation.layout.fillMaxSize", "import androidx.compose.foundation.layout.fillMaxSize" + imports_to_add)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
