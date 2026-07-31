package com.example.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Logout
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.viewmodel.InvoiceUiState
import androidx.compose.ui.res.stringResource
import com.example.R
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext



@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    state: InvoiceUiState,
    onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, swipeToDelete: Boolean) -> Unit,
    onLogout: () -> Unit,
    onBack: () -> Unit
) {
    var storeName by remember { mutableStateOf(state.storeName.ifBlank { "Quick Bill HQ" }) }
    var storeAddress by remember { mutableStateOf(state.storeAddress.ifBlank { "123 Design System Blvd, Suite 404, San Francisco, CA" }) }
    var storePhone by remember { mutableStateOf(state.storePhone.ifBlank { "+1 (555) 123-4567" }) }
    var ownerName by remember { mutableStateOf(state.ownerName.ifBlank { "Jane Doe" }) }
    var swipeToDeleteEnabled by remember { mutableStateOf(state.swipeToDeleteEnabled) }
    
    var editingField by remember { mutableStateOf<String?>(null) }
    var editValue by remember { mutableStateOf("") }
    
    val context = LocalContext.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Settings", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                    titleContentColor = MaterialTheme.colorScheme.onBackground
                )
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(bottom = 32.dp)
        ) {
            
            item {
                SectionHeader("Account")
                SettingsItem(
                    title = "Store Code",
                    subtitle = state.storeUid,
                    trailingIcon = { Icon(Icons.Default.ContentCopy, contentDescription = "Copy") },
                    onClick = {
                        val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                        val clip = ClipData.newPlainText("Store Code", state.storeUid)
                        clipboard.setPrimaryClip(clip)
                        Toast.makeText(context, "Store Code copied to clipboard", Toast.LENGTH_SHORT).show()
                    }
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
                
                ListItem(
                    headlineContent = { Text("Logout", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.error) },
                    leadingContent = { Icon(Icons.AutoMirrored.Filled.Logout, contentDescription = "Logout", tint = MaterialTheme.colorScheme.error) },
                    modifier = Modifier.clickable { onLogout() },
                    colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.background)
                )
            }
            
            item {
                Spacer(modifier = Modifier.height(16.dp))
                SectionHeader("Store Settings")
                
                SettingsItem(
                    title = "Store Name",
                    subtitle = storeName,
                    trailingIcon = { Icon(Icons.Default.Edit, contentDescription = "Edit") },
                    onClick = { editingField = "Store Name"; editValue = storeName }
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
                
                SettingsItem(
                    title = "Address",
                    subtitle = storeAddress,
                    trailingIcon = { Icon(Icons.Default.Edit, contentDescription = "Edit") },
                    onClick = { editingField = "Address"; editValue = storeAddress }
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
                
                SettingsItem(
                    title = "Phone",
                    subtitle = storePhone,
                    trailingIcon = { Icon(Icons.Default.Edit, contentDescription = "Edit") },
                    onClick = { editingField = "Phone"; editValue = storePhone }
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
                
                SettingsItem(
                    title = "Owner Name",
                    subtitle = ownerName,
                    trailingIcon = { Icon(Icons.Default.Edit, contentDescription = "Edit") },
                    onClick = { editingField = "Owner Name"; editValue = ownerName }
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
            }
            

            
            item {
                Spacer(modifier = Modifier.height(48.dp))
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(stringResource(R.string.app_name), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text("v1.0.4", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        
        if (editingField != null) {
            AlertDialog(
                onDismissRequest = { editingField = null },
                title = { Text("Edit $editingField") },
                text = {
                    OutlinedTextField(
                        value = editValue,
                        onValueChange = { editValue = it },
                        modifier = Modifier.fillMaxWidth(),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                            unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        )
                    )
                },
                confirmButton = {
                    Button(
                        onClick = {
                            when (editingField) {
                                "Store Name" -> storeName = editValue
                                "Address" -> storeAddress = editValue
                                "Phone" -> storePhone = editValue
                                "Owner Name" -> ownerName = editValue
                            }
                            onUpdateStoreSettings(storeName, storeAddress, storePhone, ownerName, swipeToDeleteEnabled)
                            editingField = null
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                    ) {
                        Text("Save")
                    }
                },
                dismissButton = {
                    TextButton(onClick = { editingField = null }) {
                        Text("Cancel", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                },
                containerColor = MaterialTheme.colorScheme.surfaceVariant
            )
        }
    }
}

@Composable
fun SectionHeader(title: String) {
    Text(
        text = title,
        style = MaterialTheme.typography.titleMedium,
        fontWeight = FontWeight.Bold,
        color = MaterialTheme.colorScheme.primary,
        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
    )
}

@Composable
fun SettingsItem(title: String, subtitle: String, trailingIcon: @Composable () -> Unit, onClick: () -> Unit) {
    ListItem(
        headlineContent = { Text(title, fontWeight = FontWeight.Bold) },
        supportingContent = { Text(subtitle, color = MaterialTheme.colorScheme.onSurfaceVariant) },
        trailingContent = trailingIcon,
        modifier = Modifier.clickable { onClick() },
        colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.background)
    )
}
