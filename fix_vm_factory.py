import re

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace("import androidx.lifecycle.ViewModel", "import androidx.lifecycle.ViewModel\nimport androidx.lifecycle.viewModelScope\nimport com.example.model.GroceryRepository\nimport kotlinx.coroutines.launch\nimport kotlinx.coroutines.flow.SharingStarted\nimport kotlinx.coroutines.flow.stateIn\nimport androidx.lifecycle.ViewModelProvider")
content = content.replace("class InvoiceViewModel : ViewModel() {", "class InvoiceViewModel(private val repository: GroceryRepository) : ViewModel() {")

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(content)
