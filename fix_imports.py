import re

def fix_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Remove all ExposedDropdownMenuBox, DropdownMenuItem, ExposedDropdownMenuDefaults, ExperimentalMaterial3Api imports
    content = re.sub(r'import androidx\.compose\.material3\.ExposedDropdownMenuBox\n?', '', content)
    content = re.sub(r'import androidx\.compose\.material3\.DropdownMenuItem\n?', '', content)
    content = re.sub(r'import androidx\.compose\.material3\.ExposedDropdownMenuDefaults\n?', '', content)
    content = re.sub(r'import androidx\.compose\.material3\.ExperimentalMaterial3Api\n?', '', content)
    
    # Put them exactly once
    content = content.replace('import androidx.compose.material3.Text', 'import androidx.compose.material3.ExposedDropdownMenuBox\nimport androidx.compose.material3.DropdownMenuItem\nimport androidx.compose.material3.ExposedDropdownMenuDefaults\nimport androidx.compose.material3.ExperimentalMaterial3Api\nimport androidx.compose.material3.Text')
    
    with open(filename, 'w') as f:
        f.write(content)

fix_file('app/src/main/java/com/example/ui/components/AddCustomItemDialog.kt')
fix_file('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt')

