package com.example.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.viewmodel.InvoiceUiState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    state: InvoiceUiState,
    onUpdateStoreSettings: (name: String, address: String, phone: String, owner: String, swipeToDelete: Boolean) -> Unit,
    onLogout: () -> Unit,
    onBack: () -> Unit
) {
    var storeName by remember { mutableStateOf(state.storeName) }
    var storeAddress by remember { mutableStateOf(state.storeAddress) }
    var storePhone by remember { mutableStateOf(state.storePhone) }
    var ownerName by remember { mutableStateOf(state.ownerName) }
    
    var swipeToDeleteEnabled by remember { mutableStateOf(state.swipeToDeleteEnabled) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Settings") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Account", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                
                OutlinedTextField(
                    value = state.storeUid,
                    onValueChange = {},
                    label = { Text("Store Code (Share this to sync with other devices)") },
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
            
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Store Settings", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                
                OutlinedTextField(
                    value = storeName,
                    onValueChange = { storeName = it },
                    label = { Text("Store Name") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = storeAddress,
                    onValueChange = { storeAddress = it },
                    label = { Text("Store Address") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = storePhone,
                    onValueChange = { storePhone = it },
                    label = { Text("Store Phone") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = ownerName,
                    onValueChange = { ownerName = it },
                    label = { Text("Owner Name") },
                    modifier = Modifier.fillMaxWidth()
                )

                
                Button(
                    onClick = { onUpdateStoreSettings(storeName, storeAddress, storePhone, ownerName, swipeToDeleteEnabled) },
                    modifier = Modifier.align(Alignment.End)
                ) {
                    Text("Save Store Settings")
                }
            }
            
            Divider()
            
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Actions Group", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Enable Swipe to Delete (Invoices/Customers)")
                    Switch(
                        checked = swipeToDeleteEnabled,
                        onCheckedChange = { swipeToDeleteEnabled = it }
                    )
                }
            }
            
            Spacer(modifier = Modifier.weight(1f))
            
            Column(
                modifier = Modifier.fillMaxWidth(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Icon(Icons.Default.Info, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("App Name: Quick Bill", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("Version: 1.0.0", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}
