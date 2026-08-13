import glob
import os

files = glob.glob('app/src/main/java/com/example/ui/screens/*.kt')

for fpath in files:
    with open(fpath, 'r') as f:
        text = f.read()

    # Replace TopAppBar background
    text = text.replace("containerColor = MaterialTheme.colorScheme.background,", "containerColor = androidx.compose.ui.graphics.Color.Transparent,")
    
    # Replace ListItemDefaults background
    text = text.replace("containerColor = MaterialTheme.colorScheme.background)", "containerColor = androidx.compose.ui.graphics.Color.Transparent)")

    # CustomersScreen specific modifier
    text = text.replace("Modifier.background(MaterialTheme.colorScheme.background)", "Modifier")

    with open(fpath, 'w') as f:
        f.write(text)

