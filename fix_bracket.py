with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

# Add java.util.Date import
if "import java.util.Date" not in text:
    text = text.replace("import java.util.Locale", "import java.util.Locale\nimport java.util.Date")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)
