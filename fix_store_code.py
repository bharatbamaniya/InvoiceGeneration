import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

imports = """import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext
"""

text = text.replace("import com.example.R", "import com.example.R\n" + imports)

# We need to add `val context = LocalContext.current` inside the SettingsScreen.
# Then update the onClick.

# Add LocalContext inside SettingsScreen
local_context_line = """    var editingField by remember { mutableStateOf<String?>(null) }
    var editValue by remember { mutableStateOf("") }
    
    val context = LocalContext.current"""

text = text.replace("""    var editingField by remember { mutableStateOf<String?>(null) }
    var editValue by remember { mutableStateOf("") }""", local_context_line)

old_store_code = """                SettingsItem(
                    title = "Store Code",
                    subtitle = "100-ABT234-8",
                    trailingIcon = { Icon(Icons.Default.ContentCopy, contentDescription = "Copy") },
                    onClick = { /* Copy */ }
                )"""

new_store_code = """                SettingsItem(
                    title = "Store Code",
                    subtitle = state.storeUid,
                    trailingIcon = { Icon(Icons.Default.ContentCopy, contentDescription = "Copy") },
                    onClick = {
                        val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                        val clip = ClipData.newPlainText("Store Code", state.storeUid)
                        clipboard.setPrimaryClip(clip)
                        Toast.makeText(context, "Store Code copied to clipboard", Toast.LENGTH_SHORT).show()
                    }
                )"""

text = text.replace(old_store_code, new_store_code)

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

