import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
imports = []
package_line = ""
for line in lines:
    if line.startswith("package "):
        package_line = line
    elif line.startswith("import "):
        imports.append(line)
    else:
        new_lines.append(line)

final_content = package_line + "\n" + "".join(imports) + "".join(new_lines)
with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(final_content)

