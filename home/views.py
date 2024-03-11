from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Category

# Create your views here.

@login_required(login_url="login")
def index(request):
    categories = Category.objects.all()
    return render(request,"index.html")

@login_required(login_url="login")
def add_expense(request):
    categories = Category.objects.all()
    context={
        'categories':categories,
    }
    return render(request,"add_expense.html",context)
