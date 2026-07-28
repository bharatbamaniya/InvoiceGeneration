import re

with open('app/src/main/java/com/example/ui/components/ItemConfigSheet.kt', 'r') as f:
    content = f.read()

new_logic = """    var selectedUnit by remember { 
        mutableStateOf(
            if (isWeight) {
                if (initialQty > 0 && initialQty < 1.0) "gm"
                else if (initialQty > 0 && (initialQty * 10).toInt() % 5 != 0) "gm"
                else "kg"
            } else item.unit
        ) 
    }"""

better_logic = """    var selectedUnit by remember { 
        mutableStateOf(
            if (isWeight) {
                if (initialQty > 0.0 && initialQty < 1.0) "gm"
                else if (initialQty > 0.0 && (initialQty * 10).toInt() % 5 != 0) "gm"
                else "kg"
            } else item.unit
        ) 
    }"""

content = content.replace(new_logic, better_logic)

with open('app/src/main/java/com/example/ui/components/ItemConfigSheet.kt', 'w') as f:
    f.write(content)

