from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import Category,Expense
from django.contrib import messages

# Create your views here.

@login_required(login_url="login")
def index(request):
    categories = Category.objects.all()
    expense = Expense.objects.filter(owner=request.user)
    
    context ={
        'expenses':expense
    }
    return render(request,"index.html",context)

@login_required(login_url="login")
def add_expense(request):
    categories = Category.objects.all()
    context={
        'categories':categories,
        'values':request.POST
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']

        if not amount:
            messages.error(request, 'Amount is Required')
            return render(request,"add_expense.html",context)
        if not description:
            messages.error(request, 'Description is Required')
            return render(request,"add_expense.html",context)
        if not date:
            messages.error(request, 'Please select expense date')
            return render(request,"add_expense.html",context)
        
        Expense.objects.create(owner=request.user,amount=amount,description=description,category=category,date=date)
        messages.success(request, 'Expense Save Successfully')
        return redirect('expences')
    return render(request,"add_expense.html",context)
    
