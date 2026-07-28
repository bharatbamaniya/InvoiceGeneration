import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add import for AuthScreen
if "import com.example.ui.screens.AuthScreen" not in content:
    content = content.replace("import com.example.ui.screens.HomeScreen", "import com.example.ui.screens.AuthScreen\nimport com.example.ui.screens.HomeScreen")

# Modify surface content
# Wait, let's find Scaffold and wrap it or just if else
auth_logic = """
            if (!uiState.isAuthenticated) {
                AuthScreen(
                    onLogin = viewModel::login,
                    onRegister = viewModel::registerNewStore
                )
            } else {
"""

# The scaffold starts around `Scaffold(`
scaffold_start = "            Scaffold("
if scaffold_start in content:
    content = content.replace(scaffold_start, auth_logic + scaffold_start)
    # now we need to add a closing brace for the else block. Let's find the end of Surface
    surface_end = """            }
        }
    }
}"""
    content = content.replace(surface_end, "                }\n            }\n        }\n    }\n}")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

