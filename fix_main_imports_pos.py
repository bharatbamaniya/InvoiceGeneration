with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

package_line_idx = -1
for i, line in enumerate(lines):
    if line.startswith('package '):
        package_line_idx = i
        break

if package_line_idx != -1:
    # move everything before package_line_idx to after it
    imports = lines[:package_line_idx]
    package_line = lines[package_line_idx]
    rest = lines[package_line_idx+1:]
    
    new_lines = [package_line] + imports + rest
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.writelines(new_lines)

