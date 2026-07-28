package com.example.model

import androidx.room.Entity
import androidx.room.PrimaryKey


@Entity(tableName = "inventory")
data class GroceryItem(
    @PrimaryKey 
    val id: String = "",
    val name: String = "",
    val price: Double = 0.0,
    val unit: String = "kg",
    val iconEmoji: String = "📦"
)

data class InvoiceItem(
    val item: GroceryItem = GroceryItem(),
    val quantity: Double = 0.0,
    val customPrice: Double? = null
) {
    val unitPrice: Double
        get() = customPrice ?: item.price

    val totalPrice: Double
        get() = unitPrice * quantity
}

@Entity(tableName = "invoices")
data class Invoice(
    @PrimaryKey 
    val invoiceId: String = "",
    val storeName: String = "",
    val storeAddress: String = "",
    val storePhone: String = "",
    val storeSubtitle: String = "Fresh Vegetable, Fruits & Exotic Vegetable Supplier",
    val ownerName: String = "Owner",
    val customerName: String = "",
    val customerPhone: String = "",
    val customerId: String? = null,
    val items: List<InvoiceItem> = emptyList(),
    val previousOutstanding: Double = 0.0,
    val cashReceived: Double = 0.0,
    val dateMillis: Long = System.currentTimeMillis(),
    val currencySymbol: String = "₹"
) {
    val billAmount: Double
        get() = items.sumOf { it.totalPrice }

    val totalBalance: Double
        get() = previousOutstanding + billAmount - cashReceived

    val totalItemCount: Double
        get() = items.sumOf { it.quantity }
}

@Entity(tableName = "customers")
data class Customer(
    @PrimaryKey 
    val id: String = "",
    val name: String = "",
    val phone: String = "",
    val balance: Double = 0.0 // positive means they owe us
)

@Entity(tableName = "payments")
data class Payment(
    @PrimaryKey 
    val id: String = "",
    val customerId: String = "",
    val amount: Double = 0.0,
    val dateMillis: Long = System.currentTimeMillis(),
    val remark: String = ""
)
