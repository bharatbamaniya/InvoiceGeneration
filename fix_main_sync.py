import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("                    HomeScreen(\n                        state = uiState,\n                        onSettingsClick =", "                    HomeScreen(\n                        state = uiState,\n                        onSyncClick = { viewModel.syncData() },\n                        onSettingsClick =")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
