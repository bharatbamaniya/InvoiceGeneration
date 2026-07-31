import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

old_dialer_logic = """                                                if (qtyStr == "0" && key != ".") {
                                                    qtyStr = key
                                                } else {
                                                    if (key == "." && qtyStr.contains(".")) {
                                                        // do nothing
                                                    } else {
                                                        qtyStr += key
                                                    }
                                                }"""

new_dialer_logic = """                                                val newStr = if (qtyStr == "0" && key != ".") {
                                                    key
                                                } else if (key == "." && qtyStr.contains(".")) {
                                                    qtyStr
                                                } else {
                                                    qtyStr + key
                                                }
                                                if ((newStr.toDoubleOrNull() ?: 0.0) <= maxValue) {
                                                    qtyStr = newStr
                                                }"""

text = text.replace(old_dialer_logic, new_dialer_logic)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)
