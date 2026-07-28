import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('label = { Text("Store UID (Share this to login elsewhere)") }', 'label = { Text("Store Code (Share this to sync with other devices)") }')

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(content)

