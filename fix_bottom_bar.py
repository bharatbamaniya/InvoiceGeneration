import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# Make the bottom bar a floating pill, correctly layered
old_scaffold_bottom = """        bottomBar = {
            if (currentScreen in listOf(AppScreen.HOME, AppScreen.CUSTOMERS)) {
                Box(
                    modifier = Modifier.fillMaxWidth().padding(16.dp).padding(bottom = 8.dp),
                    contentAlignment = Alignment.BottomCenter
                ) {
                    NavigationBar(
                        modifier = Modifier
                            .fillMaxWidth(0.6f)
                            .clip(androidx.compose.foundation.shape.RoundedCornerShape(32.dp)),
                        tonalElevation = 8.dp
                    ) {
                        NavigationBarItem(
                            selected = currentScreen == AppScreen.HOME,
                            onClick = { currentScreen = AppScreen.HOME },
                            icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                            label = { Text("Home") }
                        )
                        NavigationBarItem(
                            selected = currentScreen == AppScreen.CUSTOMERS,
                            onClick = { currentScreen = AppScreen.CUSTOMERS },
                            icon = { Icon(Icons.Default.Person, contentDescription = "Customers") },
                            label = { Text("Customers") }
                        )
                    }
                }
            }
        }"""
        
new_scaffold_bottom = "        // Bottom bar removed from scaffold to float freely"
code = code.replace(old_scaffold_bottom, new_scaffold_bottom)

old_inner = """        Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {"""
new_inner = """        Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
            // Content
            Box(modifier = Modifier.fillMaxSize()) {"""
            
old_end = """                }
            }
        }
    }
}"""
new_end = """                }
            }
            
            // Floating Bottom Bar Overlay
            if (currentScreen in listOf(AppScreen.HOME, AppScreen.CUSTOMERS)) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(bottom = 24.dp),
                    contentAlignment = Alignment.BottomCenter
                ) {
                    Surface(
                        shape = androidx.compose.foundation.shape.RoundedCornerShape(percent = 50),
                        color = MaterialTheme.colorScheme.surfaceVariant,
                        tonalElevation = 8.dp,
                        shadowElevation = 8.dp,
                        modifier = Modifier.padding(horizontal = 32.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                            horizontalArrangement = Arrangement.spacedBy(32.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            val isHome = currentScreen == AppScreen.HOME
                            Surface(
                                shape = androidx.compose.foundation.shape.RoundedCornerShape(percent = 50),
                                color = if (isHome) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent,
                                modifier = Modifier.clickable { currentScreen = AppScreen.HOME }
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Home, 
                                        contentDescription = "Home",
                                        tint = if (isHome) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    if (isHome) {
                                        Text(
                                            "Home", 
                                            fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.onSecondaryContainer
                                        )
                                    }
                                }
                            }
                            
                            val isCust = currentScreen == AppScreen.CUSTOMERS
                            Surface(
                                shape = androidx.compose.foundation.shape.RoundedCornerShape(percent = 50),
                                color = if (isCust) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent,
                                modifier = Modifier.clickable { currentScreen = AppScreen.CUSTOMERS }
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Person, 
                                        contentDescription = "Customers",
                                        tint = if (isCust) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    if (isCust) {
                                        Text(
                                            "Customers", 
                                            fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.onSecondaryContainer
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}"""
code = code.replace(old_end, new_end)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)

