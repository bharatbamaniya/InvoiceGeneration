import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    content = f.read()

pattern = r'val permissionLauncher = rememberLauncherForActivityResult.*?\}\s*\)\s*\}'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(content)

