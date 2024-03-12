from django.urls import path
from home.views import index,add_expense,expense_edit,delete_expense,search_expenses
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("",index,name="expences"),
    path("add-expense/",add_expense,name="add-expense"),
    path("expense-edit/<int:id>",expense_edit,name="expense-edit"),
    path("delete-expense/<int:id>",delete_expense,name="delete-expense"),
    path("search-expenses",csrf_exempt(search_expenses),name="search_expenses"), # type: ignore
]
