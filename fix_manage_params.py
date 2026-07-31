with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("onAddItem: (String, Double, String) -> Unit,", "onAddItem: (String, Double, String, String) -> Unit,")
text = text.replace("onConfirm: (String, Double, String) -> Unit,", "onConfirm: (String, Double, String, String) -> Unit,")

dialog_text = """                // Mock image upload area
                Column {
                    Text("Item Image (Optional)", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(4.dp))
                    Card(
                        modifier = Modifier.fillMaxWidth().height(100.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Icon(Icons.Default.Add, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("Tap to upload image", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }"""

new_dialog_text = """                Column {
                    Text("Item Image (Optional)", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(4.dp))
                    
                    val launcher = rememberLauncherForActivityResult(
                        contract = ActivityResultContracts.GetContent()
                    ) { uri ->
                        if (uri != null) {
                            imageUri = uri.toString()
                        }
                    }
                    
                    Card(
                        modifier = Modifier.fillMaxWidth().height(100.dp).clickable { launcher.launch("image/*") },
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            if (imageUri.isNotBlank()) {
                                AsyncImage(
                                    model = imageUri,
                                    contentDescription = "Item image",
                                    contentScale = ContentScale.Crop,
                                    modifier = Modifier.fillMaxSize()
                                )
                            } else {
                                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                    Icon(Icons.Default.Add, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text("Tap to upload image", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                }
                            }
                        }
                    }
                }"""

text = text.replace(dialog_text, new_dialog_text)

# Add imageUri state
state_code = """    var name by remember { mutableStateOf(item?.name ?: "") }
    var priceStr by remember { mutableStateOf(item?.price?.toString() ?: "") }
    var unit by remember { mutableStateOf(item?.unit ?: "kg") }
    var imageUri by remember { mutableStateOf(item?.iconEmoji ?: "") }"""

text = text.replace("""    var name by remember { mutableStateOf(item?.name ?: "") }
    var priceStr by remember { mutableStateOf(item?.price?.toString() ?: "") }
    var unit by remember { mutableStateOf(item?.unit ?: "kg") }""", state_code)

# Fix onConfirm
onConfirm_text = """                    if (name.isNotBlank() && price > 0) {
                        onConfirm(name, price, unit)
                    }"""
new_onConfirm = """                    if (name.isNotBlank() && price > 0) {
                        onConfirm(name, price, unit, imageUri)
                    }"""
text = text.replace(onConfirm_text, new_onConfirm)

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(text)

