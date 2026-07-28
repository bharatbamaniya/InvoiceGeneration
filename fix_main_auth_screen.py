import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("                    onRegister = viewModel::registerNewStore", "")
content = content.replace("                AuthScreen(\n                    onLogin = viewModel::login,\n\n                )", "                AuthScreen(onLogin = viewModel::login)")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

