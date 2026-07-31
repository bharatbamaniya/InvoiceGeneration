with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("            if (showSettleDialog)", "        }\n        if (showSettleDialog)")

with open('app/src/main/java/com/example/ui/screens/CustomerDetailScreen.kt', 'w') as f:
    f.write(text)
