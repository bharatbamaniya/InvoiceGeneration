import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

auth_logic = """    if (!uiState.isAuthenticated) {
        AuthScreen(
            onLogin = viewModel::login,
            onRegister = viewModel::registerNewStore
        )
        return
    }

    Scaffold("""

content = content.replace("    Scaffold(", auth_logic)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

