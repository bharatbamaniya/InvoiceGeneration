import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

pattern = r"// Real Quantity Picker.*?Surface\(\s*color = MaterialTheme\.colorScheme\.surfaceVariant,"

new_dialer = """// Real Quantity Picker
                val maxValue = 500f
                val sliderValue = (qtyStr.toFloatOrNull() ?: 0f).coerceIn(0f, maxValue)
                
                // Numpad for quantity
                Column(modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp)) {
                    val keys = listOf(
                        listOf("1", "2", "3"),
                        listOf("4", "5", "6"),
                        listOf("7", "8", "9"),
                        listOf(".", "0", "DEL")
                    )
                    
                    keys.forEach { row ->
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            horizontalArrangement = Arrangement.SpaceEvenly
                        ) {
                            row.forEach { key ->
                                Surface(
                                    modifier = Modifier
                                        .size(64.dp)
                                        .clip(RoundedCornerShape(32.dp))
                                        .clickable {
                                            if (key == "DEL") {
                                                if (qtyStr.isNotEmpty()) {
                                                    qtyStr = qtyStr.dropLast(1)
                                                    if (qtyStr.isEmpty()) qtyStr = "0"
                                                }
                                            } else {
                                                if (qtyStr == "0" && key != ".") {
                                                    qtyStr = key
                                                } else {
                                                    if (key == "." && qtyStr.contains(".")) {
                                                        // do nothing
                                                    } else {
                                                        qtyStr += key
                                                    }
                                                }
                                            }
                                        },
                                    color = MaterialTheme.colorScheme.surfaceVariant,
                                    shape = RoundedCornerShape(32.dp)
                                ) {
                                    Box(contentAlignment = Alignment.Center) {
                                        if (key == "DEL") {
                                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Delete")
                                        } else {
                                            Text(key, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                   
                Surface(
                    color = MaterialTheme.colorScheme.surfaceVariant,"""

text = re.sub(pattern, new_dialer, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
