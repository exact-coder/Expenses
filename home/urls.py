from django.urls import path
from home.views import index,add_expense,expense_edit,delete_expense,search_expenses,expense_category_summary,stats_view
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("",index,name="expences"),
    path("add-expense/",add_expense,name="add-expense"),
    path("expense-edit/<int:id>",expense_edit,name="expense-edit"),
    path("delete-expense/<int:id>",delete_expense,name="delete-expense"),
    path("stats",stats_view,name="stats"),
    path("search-expenses",csrf_exempt(search_expenses),name="search_expenses"), # type: ignore
    path("expense_category_summary",csrf_exempt(expense_category_summary),name="expense_category_summary"), # type: ignore
]
