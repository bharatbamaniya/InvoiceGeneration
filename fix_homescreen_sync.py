import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

# Add Refresh icon import
if "import androidx.compose.material.icons.filled.Refresh" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Settings", "import androidx.compose.material.icons.filled.Settings\nimport androidx.compose.material.icons.filled.Refresh")

# Add onSyncClick to parameters
content = content.replace("    onSettingsClick: () -> Unit,", "    onSyncClick: () -> Unit,\n    onSettingsClick: () -> Unit,")

# Add Refresh button before Settings
old_actions = """                actions = {
                    IconButton(onClick = onSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }"""
new_actions = """                actions = {
                    IconButton(onClick = onSyncClick) {
                        Icon(Icons.Default.Refresh, contentDescription = "Sync Data")
                    }
                    IconButton(onClick = onSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }"""
content = content.replace(old_actions, new_actions)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
