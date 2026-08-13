import glob
import os

files = glob.glob('app/src/main/java/com/example/ui/screens/*.kt')

for fpath in files:
    with open(fpath, 'r') as f:
        text = f.read()

    # Add containerColor = Color.Transparent to Scaffold if not present
    if "Scaffold(" in text and "containerColor = Color.Transparent" not in text:
        text = text.replace("Scaffold(", "Scaffold(\n        containerColor = androidx.compose.ui.graphics.Color.Transparent,")
    
    # Let's also remove overlapping background modifiers that cover everything.
    # We shouldn't remove all .background, just ones that are for the entire screen.
    # In AuthScreen, there's a Surface(color = MaterialTheme.colorScheme.background)
    if "Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background)" in text:
        text = text.replace("Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background)",
                            "Surface(modifier = Modifier.fillMaxSize(), color = androidx.compose.ui.graphics.Color.Transparent)")

    with open(fpath, 'w') as f:
        f.write(text)

