import re

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'r') as f:
    content = f.read()

content = content.replace('return prefs.getString("store_uid", null)', 'val uid = prefs.getString("store_uid", null)\n        return if (uid.isNullOrBlank()) null else uid')

with open('app/src/main/java/com/example/model/GroceryRepository.kt', 'w') as f:
    f.write(content)

