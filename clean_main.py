with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# The first floating bottom bar block starts after `GroceryInvoiceApp()\n                }\n            }`
# Let's remove it entirely up to `    }\n}\n\nenum class AppScreen` or `enum class`

start_idx = code.find('            // Floating Bottom Bar Overlay', 0, code.find('enum class AppScreen'))
if start_idx != -1:
    end_idx = code.find('        }\n    }\n}\n\nenum class AppScreen')
    if end_idx != -1:
        code = code[:start_idx] + code[end_idx:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)

