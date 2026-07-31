import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

pattern = r"// Real Quantity Picker.*?Icon\(Icons\.Default\.Edit, contentDescription = \"Edit\", modifier = Modifier\.size\(16\.dp\), tint = MaterialTheme\.colorScheme\.primary\)\s*\}\s*\}"

new_slider_and_price = """// Real Quantity Picker
                val maxValue = 500f
                val sliderValue = (qtyStr.toFloatOrNull() ?: 0f).coerceIn(0f, maxValue)
                
                Text(
                    text = qtyStr,
                    style = MaterialTheme.typography.displayMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.padding(vertical = 16.dp)
                )

                Row(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Text(maxValue.toInt().toString(), color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), fontSize = 14.sp)
                        
                        Box(
                            modifier = Modifier
                                .width(64.dp)
                                .height(200.dp)
                                .clip(RoundedCornerShape(32.dp))
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                                .pointerInput(Unit) {
                                    detectVerticalDragGestures { change, dragAmount ->
                                        change.consume()
                                        val height = size.height.toFloat()
                                        val deltaValue = (-dragAmount / height) * maxValue
                                        val newValue = (sliderValue + deltaValue).coerceIn(0f, maxValue)
                                        val intValue = newValue.toInt()
                                        qtyStr = if (newValue % 1.0 < 0.1 || newValue % 1.0 > 0.9) {
                                            intValue.toString()
                                        } else {
                                            String.format(java.util.Locale.US, "%.1f", newValue)
                                        }
                                    }
                                }
                                .pointerInput(Unit) {
                                    detectTapGestures { offset ->
                                        val height = size.height.toFloat()
                                        val fraction = 1f - (offset.y / height)
                                        val newValue = (fraction * maxValue).coerceIn(0f, maxValue)
                                        val intValue = newValue.toInt()
                                        qtyStr = if (newValue % 1.0 < 0.1 || newValue % 1.0 > 0.9) {
                                            intValue.toString()
                                        } else {
                                            String.format(java.util.Locale.US, "%.1f", newValue)
                                        }
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
                }
                
                HorizontalDivider(modifier = Modifier.padding(bottom = 16.dp))

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Price: $currencySymbol", style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold)
                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = { priceStr = it },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.width(80.dp).height(48.dp),
                        textStyle = LocalTextStyle.current.copy(fontWeight = FontWeight.Bold),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Color.Transparent,
                            unfocusedBorderColor = Color.Transparent,
                            focusedContainerColor = Color.Transparent,
                            unfocusedContainerColor = Color.Transparent
                        )
                    )
                    Icon(Icons.Default.Edit, contentDescription = "Edit", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                }"""

text = re.sub(pattern, new_slider_and_price, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

