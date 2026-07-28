import re

def fix_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    imports = [
        'import androidx.compose.material3.ExposedDropdownMenuBox',
        'import androidx.compose.material3.DropdownMenuItem',
        'import androidx.compose.material3.ExposedDropdownMenuDefaults',
        'import androidx.compose.material3.ExperimentalMaterial3Api'
    ]
    
    for imp in imports:
        content = re.sub(r'^\s*' + re.escape(imp) + r'.*\n', '', content, flags=re.MULTILINE)
    
    content = content.replace('import androidx.compose.material3.Text', 'import androidx.compose.material3.ExposedDropdownMenuBox\nimport androidx.compose.material3.DropdownMenuItem\nimport androidx.compose.material3.ExposedDropdownMenuDefaults\nimport androidx.compose.material3.ExperimentalMaterial3Api\nimport androidx.compose.material3.Text')
    
    with open(filename, 'w') as f:
        f.write(content)

fix_file('app/src/main/java/com/example/ui/components/AddCustomItemDialog.kt')
fix_file('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt')

