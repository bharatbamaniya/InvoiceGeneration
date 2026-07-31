import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

old_kg_click = """modifier = Modifier.clickable { 
                                isGm = false
                            }"""
                            
new_kg_click = """modifier = Modifier.clickable { 
                                if (isGm) {
                                    isGm = false
                                    val currentGm = qtyStr.toFloatOrNull() ?: 0f
                                    qtyStr = String.format(java.util.Locale.US, "%.1f", currentGm / 1000f)
                                }
                            }"""

old_gm_click = """modifier = Modifier.clickable { 
                                isGm = true
                            }"""

new_gm_click = """modifier = Modifier.clickable { 
                                if (!isGm) {
                                    isGm = true
                                    val currentKg = qtyStr.toFloatOrNull() ?: 0f
                                    qtyStr = (currentKg * 1000f).toInt().toString()
                                }
                            }"""

text = text.replace(old_kg_click, new_kg_click)
text = text.replace(old_gm_click, new_gm_click)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
