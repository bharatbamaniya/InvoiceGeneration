import re

with open('app/src/main/java/com/example/model/GroceryModels.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val amount: Double = 0.0,\n    val dateMillis: Long = System.currentTimeMillis()',
    'val amount: Double = 0.0,\n    val dateMillis: Long = System.currentTimeMillis(),\n    val remark: String = ""'
)

with open('app/src/main/java/com/example/model/GroceryModels.kt', 'w') as f:
    f.write(content)
