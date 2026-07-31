import re

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    text = f.read()

imports = """import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale
import androidx.compose.foundation.clickable
"""

text = text.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\n" + imports)

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(text)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text2 = f.read()
    
text2 = text2.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\n" + imports)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text2)

