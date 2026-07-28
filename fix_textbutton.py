import re

def fix_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    if 'import androidx.compose.material3.TextButton' not in content:
        content = content.replace('import androidx.compose.material3.Text', 'import androidx.compose.material3.Text\nimport androidx.compose.material3.TextButton')
    
    with open(filename, 'w') as f:
        f.write(content)

fix_file('app/src/main/java/com/example/ui/components/AddCustomItemDialog.kt')
fix_file('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt')

