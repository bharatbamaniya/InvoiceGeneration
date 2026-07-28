package com.example.model

import androidx.room.TypeConverter
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

class Converters {
    private val gson = Gson()

    @TypeConverter
    fun fromInvoiceItemList(value: List<InvoiceItem>?): String {
        return gson.toJson(value)
    }

    @TypeConverter
    fun toInvoiceItemList(value: String): List<InvoiceItem> {
        val type = object : TypeToken<List<InvoiceItem>>() {}.type
        return gson.fromJson(value, type) ?: emptyList()
    }
}
