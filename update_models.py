with open('app/src/main/java/com/example/model/GroceryModels.kt', 'r') as f:
    content = f.read()

new_models = """
data class Customer(
    val id: String,
    val name: String,
    val phone: String,
    val balance: Double = 0.0 // positive means they owe us
)

data class Payment(
    val id: String,
    val customerId: String,
    val amount: Double,
    val dateMillis: Long = System.currentTimeMillis()
)
"""

if "data class Customer" not in content:
    content += new_models

with open('app/src/main/java/com/example/model/GroceryModels.kt', 'w') as f:
    f.write(content)
