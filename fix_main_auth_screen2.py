import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_auth = """        AuthScreen(
            onLogin = viewModel::login,
            onRegister = viewModel::registerNewStore
        )"""
new_auth = "        AuthScreen(onLogin = viewModel::login)"

content = content.replace(old_auth, new_auth)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

