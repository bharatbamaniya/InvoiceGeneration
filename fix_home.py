import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

# I want to add some animation and modern gradient to the background of HomeScreen.

new_scaffold = """
    Scaffold(
        containerColor = Color.Transparent,
        topBar = {
"""

text = text.replace("""    Scaffold(
        topBar = {""", new_scaffold)

surface_wrap_start = """
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(
                        MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.2f),
                        MaterialTheme.colorScheme.background,
                        MaterialTheme.colorScheme.background
                    )
                )
            )
    ) {
"""

text = text.replace("    Scaffold(", surface_wrap_start + "    Scaffold(")
text = text.replace("        }\n    }\n}\n", "        }\n    }\n}\n}\n")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

