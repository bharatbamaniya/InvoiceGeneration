import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

text = text.replace("""                    GroceryInvoiceApp()
                }
            }
        }
    }
}
@Composable""", """                    GroceryInvoiceApp()
                }
                }
            }
        }
    }
}
@Composable""")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)

