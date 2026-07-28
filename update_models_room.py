import re

with open('app/src/main/java/com/example/model/GroceryModels.kt', 'r') as f:
    content = f.read()

imports = """package com.example.model

import androidx.room.Entity
import androidx.room.PrimaryKey
"""

content = content.replace("package com.example.model", imports)

content = content.replace("data class GroceryItem(", "@Entity(tableName = \"inventory\")\ndata class GroceryItem(\n    @PrimaryKey ")
content = content.replace("data class Invoice(", "@Entity(tableName = \"invoices\")\ndata class Invoice(\n    @PrimaryKey ")
content = content.replace("data class Customer(", "@Entity(tableName = \"customers\")\ndata class Customer(\n    @PrimaryKey ")
content = content.replace("data class Payment(", "@Entity(tableName = \"payments\")\ndata class Payment(\n    @PrimaryKey ")

with open('app/src/main/java/com/example/model/GroceryModels.kt', 'w') as f:
    f.write(content)
