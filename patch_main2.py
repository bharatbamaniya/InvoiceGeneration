import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

code = re.sub(
    r'onNewSale = \{.*?\},',
    r'',
    code,
    flags=re.DOTALL
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)

