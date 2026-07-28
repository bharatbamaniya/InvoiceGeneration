import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main_content = f.read()
    
main_content = main_content.replace(
    'onSettleBalance = { amount -> viewModel.settleCustomerBalance(customer.id, amount) },',
    'onSettleBalance = { amount, remark -> viewModel.settleCustomerBalance(customer.id, amount, remark) },'
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main_content)


with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'r') as f:
    vm_content = f.read()

vm_content = vm_content.replace(
    'fun settleCustomerBalance(customerId: String, amount: Double) {',
    'fun settleCustomerBalance(customerId: String, amount: Double, remark: String = "") {'
)

vm_content = vm_content.replace(
    '            amount = amount\n        )',
    '            amount = amount,\n            remark = remark\n        )'
)

with open('app/src/main/java/com/example/viewmodel/InvoiceViewModel.kt', 'w') as f:
    f.write(vm_content)
