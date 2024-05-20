from django.urls import path
from userincome.views import index,add_income,income_edit,delete_income,search_incomes
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("",index,name="income"),
    path("add-income/",add_income,name="add-income"),
    path("income-edit/<int:id>",income_edit,name="income-edit"),
    path("delete-income/<int:id>",delete_income,name="delete-income"),
    path("search-incomes",csrf_exempt(search_incomes),name="search_incomes"), # type: ignore
]
