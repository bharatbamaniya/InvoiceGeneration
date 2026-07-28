import re

def clean_imports(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Remove all known duplicated material3 imports
    imports_to_remove = [
        "import androidx.compose.material3.ExposedDropdownMenuBox",
        "import androidx.compose.material3.DropdownMenuItem",
        "import androidx.compose.material3.ExposedDropdownMenuDefaults",
        "import androidx.compose.material3.ExperimentalMaterial3Api",
        "import androidx.compose.material3.Text"
    ]
    
    for imp in imports_to_remove:
        content = re.sub(r'^\s*' + re.escape(imp) + r'.*\n', '', content, flags=re.MULTILINE)
    
    # Insert them back ONCE after import androidx.compose.material3.OutlinedTextField
    insertion = "\n".join(imports_to_remove) + "\n"
    content = content.replace("import androidx.compose.material3.OutlinedTextField", "import androidx.compose.material3.OutlinedTextField\n" + insertion)
    
    with open(filename, 'w') as f:
        f.write(content)

clean_imports('app/src/main/java/com/example/ui/components/AddCustomItemDialog.kt')
clean_imports('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt')
