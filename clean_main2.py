import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# I will find `// Floating Bottom Bar Overlay` which appears twice, and remove the first occurrence.
occurrences = [m.start() for m in re.finditer(r'// Floating Bottom Bar Overlay', code)]
if len(occurrences) > 1:
    # First occurrence is around line 84
    start = occurrences[0]
    # End of that block is before `enum class AppScreen`
    end = code.find('    }\n}\n\nenum class AppScreen')
    code = code[:start] + '        }\n' + code[end:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
