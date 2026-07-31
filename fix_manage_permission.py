import re

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    text = f.read()

if "import androidx.compose.ui.platform.LocalContext" not in text:
    text = text.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.platform.LocalContext")

old_launcher = """                    val launcher = rememberLauncherForActivityResult(
                        contract = ActivityResultContracts.GetContent()
                    ) { uri ->
                        if (uri != null) {
                            imageUri = uri.toString()
                        }
                    }"""

new_launcher = """                    val context = LocalContext.current
                    val launcher = rememberLauncherForActivityResult(
                        contract = ActivityResultContracts.GetContent()
                    ) { uri ->
                        if (uri != null) {
                            try {
                                context.contentResolver.takePersistableUriPermission(
                                    uri, 
                                    android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION
                                )
                            } catch (e: Exception) {}
                            imageUri = uri.toString()
                        }
                    }"""

text = text.replace(old_launcher, new_launcher)

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(text)

