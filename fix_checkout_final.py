import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    content = f.read()

# Add missing imports for KeyboardOptions
if "import androidx.compose.foundation.text.KeyboardOptions" not in content:
    content = "import androidx.compose.foundation.text.KeyboardOptions\n" + content
if "import androidx.compose.ui.text.input.KeyboardType" not in content:
    content = "import androidx.compose.ui.text.input.KeyboardType\n" + content
if "import androidx.compose.material.icons.filled.KeyboardArrowDown" not in content:
    content = "import androidx.compose.material.icons.filled.KeyboardArrowDown\n" + content
if "import androidx.compose.material.icons.filled.KeyboardArrowUp" not in content:
    content = "import androidx.compose.material.icons.filled.KeyboardArrowUp\n" + content


# Remove getContactDetails
get_contact_pattern = r'// Helper function to read contact\nfun getContactDetails.*?return Pair\(name, phone\)\n}'
content = re.sub(get_contact_pattern, '', content, flags=re.DOTALL)

# Remove contactPickerLauncher
launcher_pattern = r'val contactPickerLauncher = rememberLauncherForActivityResult.*?\)\s*\}\s*\)'
content = re.sub(launcher_pattern, '', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(content)

