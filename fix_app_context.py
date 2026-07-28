import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("val repository = GroceryRepository(database, applicationContext)", "val repository = GroceryRepository(database, context.applicationContext)")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

