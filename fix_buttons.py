import os

files_to_fix = [
    'app/src/main/java/com/example/ui/screens/SettingsScreen.kt',
    'app/src/main/java/com/example/ui/screens/InvoiceHistoryScreen.kt',
    'app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt'
]

for file in files_to_fix:
    with open(file, 'r') as f:
        code = f.read()
    
    # Fix buttons
    code = code.replace('IconElevatedButton', 'IconButton')
    code = code.replace('TextElevatedButton', 'TextButton')
    
    # Check if ElevatedCard is used but not imported
    if 'ElevatedCard' in code and 'import androidx.compose.material3.ElevatedCard' not in code:
        code = code.replace('import androidx.compose.material3.Card', 'import androidx.compose.material3.Card\nimport androidx.compose.material3.ElevatedCard')
        
    if 'CenterAlignedTopAppBar' in code and 'import androidx.compose.material3.CenterAlignedTopAppBar' not in code:
        code = code.replace('import androidx.compose.material3.TopAppBar', 'import androidx.compose.material3.TopAppBar\nimport androidx.compose.material3.CenterAlignedTopAppBar')
        
    with open(file, 'w') as f:
        f.write(code)

