import re

def fix_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # replace modifier = Modifier.menuAnchor() with modifier = Modifier.menuAnchor()
    # actually, in the new compose Material3, menuAnchor takes (type: MenuAnchorType, enabled: Boolean)
    # wait, the warning said: Use overload that takes MenuAnchorType and enabled parameters.
    # so we can use menuAnchor(MenuAnchorType.PrimaryNotEditable)
    
    if "import androidx.compose.material3.MenuAnchorType" not in content:
        content = content.replace("import androidx.compose.material3.ExposedDropdownMenuBox", "import androidx.compose.material3.MenuAnchorType\nimport androidx.compose.material3.ExposedDropdownMenuBox")
        
    content = content.replace('Modifier.menuAnchor()', 'Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable)')
    
    with open(filename, 'w') as f:
        f.write(content)

fix_file('app/src/main/java/com/example/ui/components/AddCustomItemDialog.kt')
fix_file('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt')
