import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

# Make the gradient more noticeable
old_grad = """                                colors = listOf(
                                    MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f),
                                    MaterialTheme.colorScheme.background,
                                    MaterialTheme.colorScheme.background
                                )"""

new_grad = """                                colors = listOf(
                                    MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.6f),
                                    MaterialTheme.colorScheme.tertiaryContainer.copy(alpha = 0.3f),
                                    MaterialTheme.colorScheme.background
                                )"""

text = text.replace(old_grad, new_grad)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)

