import re

with open('app/src/main/java/com/example/model/AppDatabase.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'version = 1,',
    'version = 2,'
)

content = content.replace(
    '                    "grocery_database"\n                ).build()',
    '                    "grocery_database"\n                ).fallbackToDestructiveMigration().build()'
)

with open('app/src/main/java/com/example/model/AppDatabase.kt', 'w') as f:
    f.write(content)
