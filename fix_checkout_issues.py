import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

# Fix ModalBottomSheet
old_sheet = """    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = androidx.compose.ui.graphics.Color.Transparent,"""
new_sheet = """    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = MaterialTheme.colorScheme.surface,"""
text = text.replace(old_sheet, new_sheet)

# Fix Price OutlinedTextField
old_price = """                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = { priceStr = it },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.width(80.dp).height(48.dp),
                        textStyle = LocalTextStyle.current.copy(fontWeight = FontWeight.Bold),"""

new_price = """                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = { priceStr = it },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.width(100.dp),
                        singleLine = true,
                        textStyle = LocalTextStyle.current.copy(fontWeight = FontWeight.Bold),"""
text = text.replace(old_price, new_price)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

