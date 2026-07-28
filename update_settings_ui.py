import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    content = f.read()

# Add storeUid display and logout button
auth_section = """            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Account", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                
                OutlinedTextField(
                    value = state.storeUid,
                    onValueChange = {},
                    label = { Text("Store UID (Share this to login elsewhere)") },
                    modifier = Modifier.fillMaxWidth(),
                    readOnly = true
                )
                
                Button(
                    onClick = onLogout,
                    modifier = Modifier.align(Alignment.End),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                ) {
                    Text("Logout")
                }
            }
            
            Divider()
            
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {"""

content = content.replace("            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {\n                Text(\"Store Settings\"", auth_section + "\n                Text(\"Store Settings\"")

# Add onLogout param to SettingsScreen
content = content.replace("    onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, swipeToDelete: Boolean) -> Unit,\n    onBack: () -> Unit", "    onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, swipeToDelete: Boolean) -> Unit,\n    onLogout: () -> Unit,\n    onBack: () -> Unit")

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(content)

