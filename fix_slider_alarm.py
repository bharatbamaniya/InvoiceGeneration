import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

old_unit_toggle = """                // Unit toggle
                if (item.unit == "kg") {
                    Row(
                        modifier = Modifier.padding(bottom = 24.dp).background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(24.dp))
                    ) {
                        Surface(
                            color = if (!isGm) MaterialTheme.colorScheme.primary else Color.Transparent,
                            shape = RoundedCornerShape(24.dp),
                            modifier = Modifier.clickable { 
                                isGm = false
                                val qty = qtyStr.toDoubleOrNull() ?: 0.0
                                if (qty > 10) qtyStr = (qty / 1000.0).toString()
                            }
                        ) {
                            Text("kg", modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp), color = if (!isGm) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                        Surface(
                            color = if (isGm) MaterialTheme.colorScheme.primary else Color.Transparent,
                            shape = RoundedCornerShape(24.dp),
                            modifier = Modifier.clickable { 
                                isGm = true
                                val qty = qtyStr.toDoubleOrNull() ?: 0.0
                                if (qty < 10) qtyStr = (qty * 1000.0).toString()
                            }
                        ) {
                            Text("gm", modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp), color = if (isGm) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                    }
                }"""

new_unit_toggle = """                // Unit toggle
                if (item.unit == "kg") {
                    Row(
                        modifier = Modifier.padding(bottom = 24.dp).background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(24.dp))
                    ) {
                        Surface(
                            color = if (!isGm) MaterialTheme.colorScheme.primary else Color.Transparent,
                            shape = RoundedCornerShape(24.dp),
                            modifier = Modifier.clickable { 
                                isGm = false
                            }
                        ) {
                            Text("kg", modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp), color = if (!isGm) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                        Surface(
                            color = if (isGm) MaterialTheme.colorScheme.primary else Color.Transparent,
                            shape = RoundedCornerShape(24.dp),
                            modifier = Modifier.clickable { 
                                isGm = true
                            }
                        ) {
                            Text("gm", modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp), color = if (isGm) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                    }
                }"""

if old_unit_toggle in text:
    print("Found unit toggle")
    text = text.replace(old_unit_toggle, new_unit_toggle)
else:
    print("Unit toggle not found")

old_slider = """                // Real Quantity Picker
                var sliderValue by remember { mutableStateOf((qtyStr.toFloatOrNull() ?: 1f).coerceIn(0f, 100f)) }
                   
                Row(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Text("100", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), fontSize = 14.sp)
                        Box(modifier = Modifier.width(48.dp).height(200.dp), contentAlignment = Alignment.Center) {
                            Slider(
                                value = sliderValue,
                                onValueChange = { 
                                    sliderValue = it
                                    qtyStr = String.format(Locale.US, "%.1f", it)
                                },
                                valueRange = 0f..100f,
                                modifier = Modifier
                                    .requiredWidth(200.dp)
                                    .graphicsLayer { rotationZ = -90f }
                            )
                        }
                        Text("0", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), fontSize = 14.sp)
                    }
                }"""

new_slider = """                // Real Quantity Picker
                val maxValue = 500f
                val sliderValue = (qtyStr.toFloatOrNull() ?: 0f).coerceIn(0f, maxValue)
                
                Row(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(
                        onClick = { 
                            val current = qtyStr.toFloatOrNull() ?: 0f
                            qtyStr = String.format(Locale.US, "%.1f", (current - 1f).coerceAtLeast(0f))
                        },
                        modifier = Modifier.size(48.dp)
                    ) {
                        Text("-", fontSize = 28.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    
                    Spacer(modifier = Modifier.width(24.dp))
                    
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Text(maxValue.toInt().toString(), color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), fontSize = 14.sp)
                        
                        Box(
                            modifier = Modifier
                                .width(64.dp)
                                .height(200.dp)
                                .androidx.compose.ui.draw.clip(RoundedCornerShape(32.dp))
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                                .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                    androidx.compose.foundation.gestures.detectVerticalDragGestures { change, dragAmount ->
                                        change.consume()
                                        val height = size.height.toFloat()
                                        val deltaValue = (-dragAmount / height) * maxValue
                                        val newValue = (sliderValue + deltaValue).coerceIn(0f, maxValue)
                                        qtyStr = String.format(Locale.US, "%.1f", newValue)
                                    }
                                }
                                .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                    androidx.compose.foundation.gestures.detectTapGestures { offset ->
                                        val height = size.height.toFloat()
                                        val fraction = 1f - (offset.y / height)
                                        val newValue = (fraction * maxValue).coerceIn(0f, maxValue)
                                        qtyStr = String.format(Locale.US, "%.1f", newValue)
                                    }
                                },
                            contentAlignment = Alignment.BottomCenter
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .fillMaxHeight(fraction = (sliderValue / maxValue).coerceIn(0f, 1f))
                                    .background(MaterialTheme.colorScheme.primary)
                            )
                        }
                        
                        Text("0", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), fontSize = 14.sp)
                    }
                    
                    Spacer(modifier = Modifier.width(24.dp))
                    
                    IconButton(
                        onClick = { 
                            val current = qtyStr.toFloatOrNull() ?: 0f
                            qtyStr = String.format(Locale.US, "%.1f", (current + 1f).coerceAtMost(maxValue))
                        },
                        modifier = Modifier.size(48.dp)
                    ) {
                        Text("+", fontSize = 28.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }"""

# Try a regex if exact match fails
if old_slider in text:
    print("Found exact slider match")
    text = text.replace(old_slider, new_slider)
else:
    print("Slider not exact match, using regex")
    pattern = r"// Real Quantity Picker(.*?)// Price input"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        print("Regex found slider block")
        # We need to only replace until Surface
        surface_pattern = r"// Real Quantity Picker(.*?)Surface\("
        s_match = re.search(surface_pattern, text, re.DOTALL)
        if s_match:
            print("Surface match found")
            text = text[:s_match.start()] + new_slider + "\n                   \n                Surface(" + text[s_match.end():]

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

