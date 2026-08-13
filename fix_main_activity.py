import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

old_content = """                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {"""

new_content = """                androidx.compose.foundation.layout.Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .androidx.compose.foundation.background(
                            brush = androidx.compose.ui.graphics.Brush.verticalGradient(
                                colors = listOf(
                                    MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f),
                                    MaterialTheme.colorScheme.background,
                                    MaterialTheme.colorScheme.background
                                )
                            )
                        )
                ) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color.Transparent
                ) {"""

text = text.replace(old_content, new_content)

# close the Box correctly
text = text.replace("""                }
            }
        }
    }
}

@Composable""", """                }
                }
            }
        }
    }
}

@Composable""")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)

