from django.urls import path
from userincome.views import index,add_income

urlpatterns = [
    path("",index,name="income"),
    path("add-income/",add_income,name="add-income"),
    # path("expense-edit/<int:id>",expense_edit,name="expense-edit"),
    # path("delete-expense/<int:id>",delete_expense,name="delete-expense"),
    # path("search-expenses",csrf_exempt(search_expenses),name="search_expenses"), # type: ignore
]
