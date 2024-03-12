from django.urls import path
from home.views import index,add_expense,expense_edit,delete_expense

urlpatterns = [
    path("",index,name="expences"),
    path("add-expense/",add_expense,name="add-expense"),
    path("expense-edit/<int:id>",expense_edit,name="expense-edit"),
    path("delete-expense/<int:id>",delete_expense,name="delete-expense"),
]
