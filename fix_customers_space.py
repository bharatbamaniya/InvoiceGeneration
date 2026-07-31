import re

with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'r') as f:
    code = f.read()

# Make the left part take up remaining space
code = code.replace(
    'Row(verticalAlignment = Alignment.CenterVertically) {',
    'Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {'
)

# And restrict the Text max lines so it truncates
code = code.replace(
    'Text(customer.name, fontWeight = FontWeight.Bold)',
    'Text(customer.name, fontWeight = FontWeight.Bold, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)'
)

# Also let's increase the space between them just in case
code = code.replace(
    'Spacer(modifier = Modifier.width(16.dp))',
    'Spacer(modifier = Modifier.width(16.dp))' # Keep the same
)

with open('app/src/main/java/com/example/ui/screens/CustomersScreen.kt', 'w') as f:
    f.write(code)

