from django.urls import path
from home.views import index,add_expense,expense_edit,delete_expense,search_expenses,expense_category_summary,stats_view,export_csv,export_excel,export_pdf
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("",index,name="expences"),
    path("add-expense/",add_expense,name="add-expense"),
    path("expense-edit/<int:id>",expense_edit,name="expense-edit"),
    path("delete-expense/<int:id>",delete_expense,name="delete-expense"),
    path("stats",stats_view,name="stats"),
    path("export-csv",export_csv,name="export-csv"),
    path("export-excel",export_excel,name="export-excel"),
    path("export-pdf",export_pdf,name="export-pdf"),
    path("search-expenses",csrf_exempt(search_expenses),name="search_expenses"), # type: ignore
    path("expense_category_summary",csrf_exempt(expense_category_summary),name="expense_category_summary"), # type: ignore
]
