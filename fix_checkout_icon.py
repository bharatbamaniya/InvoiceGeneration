import re

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'r') as f:
    text = f.read()

imports = """import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale
import androidx.compose.foundation.background
import androidx.compose.ui.draw.clip
"""
if "import coil.compose.AsyncImage" not in text:
    text = text.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\n" + imports)

# 1st replacement
replacement1 = """                                Box(contentAlignment = Alignment.Center) {
                                    if (item.iconEmoji.startsWith("content://") || item.iconEmoji.startsWith("http")) {
                                        AsyncImage(
                                            model = item.iconEmoji,
                                            contentDescription = item.name,
                                            contentScale = ContentScale.Crop,
                                            modifier = Modifier.fillMaxSize()
                                        )
                                    } else {
                                        Text(
                                            item.name.take(1).uppercase(), 
                                            fontWeight = FontWeight.Bold,
                                            style = MaterialTheme.typography.labelLarge,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }
                                }"""
text = text.replace("""                                Box(contentAlignment = Alignment.Center) {
                                    Text(
                                        item.name.take(1).uppercase(), 
                                        fontWeight = FontWeight.Bold,
                                        style = MaterialTheme.typography.labelLarge,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }""", replacement1)

# 2nd replacement
replacement2 = """                    Box(contentAlignment = Alignment.Center) {
                        if (item.iconEmoji.startsWith("content://") || item.iconEmoji.startsWith("http")) {
                            AsyncImage(
                                model = item.iconEmoji,
                                contentDescription = item.name,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier.fillMaxSize()
                            )
                        } else {
                            Text(item.name.take(1).uppercase(), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }"""
text = text.replace("""                    Box(contentAlignment = Alignment.Center) {
                        Text(item.name.take(1).uppercase(), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }""", replacement2)

# 3rd replacement
replacement3 = """                                Box(contentAlignment = Alignment.Center) {
                                    if (cartItem.item.iconEmoji.startsWith("content://") || cartItem.item.iconEmoji.startsWith("http")) {
                                        AsyncImage(
                                            model = cartItem.item.iconEmoji,
                                            contentDescription = cartItem.item.name,
                                            contentScale = ContentScale.Crop,
                                            modifier = Modifier.fillMaxSize()
                                        )
                                    } else {
                                        Text(cartItem.item.name.take(1).uppercase(), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    }
                                }"""
text = text.replace("""                                Box(contentAlignment = Alignment.Center) {
                                    Text(cartItem.item.name.take(1).uppercase(), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                }""", replacement3)

with open('app/src/main/java/com/example/ui/screens/CheckoutScreen.kt', 'w') as f:
    f.write(text)

