with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    code = f.read()

code = code.replace(
    'val receivedToday = todayInvoices.sumOf { it.billAmount - (it.totalBalance - it.prevOutstanding) }',
    'val receivedToday = todayInvoices.sumOf { it.billAmount - (it.totalBalance - it.previousOutstanding) }'
)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(code)
