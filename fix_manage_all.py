import re

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    text = f.read()

# I will fix the extra braces around the file.
# Since my previous `replace` ran twice, it turned 3 braces into 4, and 4 into 5.

# Let's fix line 168
text = text.replace("                        }\n                    }\n                }\n                }\n            }\n        }\n\n        if (showDialog) {", "                        }\n                    }\n                }\n            }\n        }\n\n        if (showDialog) {")

# Let's fix the ItemDialog
bad_dialog_text = """                }
                }
                   
                // Mock image upload area"""
good_dialog_text = """                }
                   
                // Mock image upload area"""
text = text.replace(bad_dialog_text, good_dialog_text)

bad_dialog_end = """                }
                }
            }
        },
        confirmButton = {"""
good_dialog_end = """                }
            }
        },
        confirmButton = {"""
text = text.replace(bad_dialog_end, good_dialog_end)

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(text)

