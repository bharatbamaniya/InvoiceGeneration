import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    content = f.read()

# Remove unused parameters from CheckoutScreen signature
content = content.replace("    onUpdateCustomerName: (String) -> Unit,\n", "")
content = content.replace("    onUpdateCustomerPhone: (String) -> Unit,\n", "")
content = content.replace("    onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, currency: String) -> Unit,\n", "")
content = content.replace("    onOpenHistory: () -> Unit,\n", "")

# Remove the unused val/vars
content = content.replace("    var showStoreSettingsDialog by remember { mutableStateOf(false) }\n", "")
content = content.replace("    var isCustomerDetailsExpanded by remember { mutableStateOf(false) }\n", "")

# Remove the dialog
dialog_str = """    if (showStoreSettingsDialog) {
        StoreSettingsDialog(
            currentName = state.storeName,
            currentAddress = state.storeAddress,
            currentPhone = state.storePhone,
            currentOwner = state.ownerName,
            currentCurrency = state.currencySymbol,
            onDismiss = { showStoreSettingsDialog = false },
            onSave = onUpdateStoreSettings
        )
    }"""
content = content.replace(dialog_str, "")

# Remove contactPickerLauncher
launcher_str = """    val contactPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickContact(),
        onResult = { uri ->
            if (uri != null) {
                val details = getContactDetails(context, uri)
                onUpdateCustomerName(details.first)
                onUpdateCustomerPhone(details.second)
            }
        }
    )"""
content = content.replace(launcher_str, "")

# Remove getContactDetails function and imports
imports_to_remove = [
    "import android.content.Context\n",
    "import android.net.Uri\n",
    "import android.provider.ContactsContract\n",
    "import androidx.activity.compose.rememberLauncherForActivityResult\n",
    "import androidx.activity.result.contract.ActivityResultContracts\n",
    "import androidx.compose.animation.AnimatedVisibility\n",
    "import androidx.compose.animation.slideInVertically\n",
    "import androidx.compose.animation.slideOutVertically\n",
    "import androidx.compose.foundation.text.KeyboardOptions\n",
    "import androidx.compose.material.icons.filled.Contacts\n",
    "import androidx.compose.material.icons.filled.History\n",
    "import androidx.compose.material.icons.filled.KeyboardArrowDown\n",
    "import androidx.compose.material.icons.filled.KeyboardArrowUp\n",
    "import androidx.compose.material.icons.filled.Person\n",
    "import androidx.compose.material.icons.filled.Phone\n",
    "import androidx.compose.material.icons.filled.Settings\n",
    "import androidx.compose.ui.text.input.KeyboardType\n",
    "import com.example.ui.components.StoreSettingsDialog\n"
]
for imp in imports_to_remove:
    content = content.replace(imp, "")

func_str = """// Helper function to read contact
fun getContactDetails(context: Context, contactUri: Uri): Pair<String, String> {
    var name = ""
    var phone = ""
    
    try {
        val cursor = context.contentResolver.query(contactUri, null, null, null, null)
        cursor?.use {
            if (it.moveToFirst()) {
                val idIndex = it.getColumnIndex(ContactsContract.Contacts._ID)
                val hasPhoneIndex = it.getColumnIndex(ContactsContract.Contacts.HAS_PHONE_NUMBER)
                val nameIndex = it.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME)
                
                val id = if (idIndex >= 0) it.getString(idIndex) else ""
                val hasPhone = if (hasPhoneIndex >= 0) it.getString(hasPhoneIndex) else "0"
                name = if (nameIndex >= 0) it.getString(nameIndex) ?: "" else ""
                
                if (hasPhone == "1") {
                    val phones = context.contentResolver.query(
                        ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                        null,
                        ContactsContract.CommonDataKinds.Phone.CONTACT_ID + " = " + id,
                        null,
                        null
                    )
                    phones?.use { pCursor ->
                        if (pCursor.moveToFirst()) {
                            val pIndex = pCursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER)
                            if (pIndex >= 0) {
                                phone = pCursor.getString(pIndex) ?: ""
                            }
                        }
                    }
                }
            }
        }
    } catch (e: Exception) {
        e.printStackTrace()
    }
    
    return Pair(name, phone)
}"""
content = content.replace(func_str, "")

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(content)

