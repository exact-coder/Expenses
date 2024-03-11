from django.urls import path
from home.views import index,add_expense

urlpatterns = [
    path("",index,name="expences"),
    path("add-expense/",add_expense,name="add-expense"),
]
