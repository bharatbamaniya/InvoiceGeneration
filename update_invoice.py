with open('app/src/main/java/com/example/model/GroceryModels.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val customerPhone: String,',
    'val customerPhone: String,\n    val customerId: String? = null,'
)

with open('app/src/main/java/com/example/model/GroceryModels.kt', 'w') as f:
    f.write(content)
