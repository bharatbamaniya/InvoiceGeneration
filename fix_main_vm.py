import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

imports = """import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.model.AppDatabase
import com.example.model.GroceryRepository"""

content = content.replace("import com.example.model.Invoice", imports + "\nimport com.example.model.Invoice")

factory = """
class InvoiceViewModelFactory(private val repository: GroceryRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(InvoiceViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return InvoiceViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
"""

content = content.replace("enum class AppScreen {", factory + "\nenum class AppScreen {")

grocery_app = """@Composable
fun GroceryInvoiceApp() {
    val context = LocalContext.current
    val database = AppDatabase.getDatabase(context)
    val repository = GroceryRepository(database)
    val viewModel: InvoiceViewModel = viewModel(factory = InvoiceViewModelFactory(repository))

    val uiState by viewModel.uiState.collectAsState()"""

content = content.replace("""@Composable
fun GroceryInvoiceApp(viewModel: InvoiceViewModel = viewModel()) {
    val context = LocalContext.current
    val uiState by viewModel.uiState.collectAsState()""", grocery_app)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
