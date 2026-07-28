import re

with open('app/src/main/java/com/example/model/GroceryModels.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val id: String,\n    val name: String,\n    val price: Double,',
    'val id: String = "",\n    val name: String = "",\n    val price: Double = 0.0,'
)

content = content.replace(
    'val item: GroceryItem,\n    val quantity: Double,',
    'val item: GroceryItem = GroceryItem(),\n    val quantity: Double = 0.0,'
)

content = content.replace(
    'val invoiceId: String,\n    val storeName: String,\n    val storeAddress: String,\n    val storePhone: String,',
    'val invoiceId: String = "",\n    val storeName: String = "",\n    val storeAddress: String = "",\n    val storePhone: String = "",'
)

content = content.replace(
    'val ownerName: String = "Owner",\n    val customerName: String,\n    val customerPhone: String,',
    'val ownerName: String = "Owner",\n    val customerName: String = "",\n    val customerPhone: String = "",'
)

content = content.replace(
    'val customerId: String? = null,\n    val items: List<InvoiceItem>,',
    'val customerId: String? = null,\n    val items: List<InvoiceItem> = emptyList(),'
)

content = content.replace(
    'val id: String,\n    val name: String,\n    val phone: String,',
    'val id: String = "",\n    val name: String = "",\n    val phone: String = "",'
)

content = content.replace(
    'val id: String,\n    val customerId: String,\n    val amount: Double,',
    'val id: String = "",\n    val customerId: String = "",\n    val amount: Double = 0.0,'
)

with open('app/src/main/java/com/example/model/GroceryModels.kt', 'w') as f:
    f.write(content)
