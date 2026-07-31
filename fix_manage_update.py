with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("onAddItem(name, price, unit)", "onAddItem(name, price, unit, imageUri)")
text = text.replace("onUpdateItem(editingItem!!.copy(name = name, price = price, unit = unit))", "onUpdateItem(editingItem!!.copy(name = name, price = price, unit = unit, iconEmoji = imageUri))")

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.write(text)

