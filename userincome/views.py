from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from userincome.models import Source,UserIncome
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
# Create your views here.


@login_required(login_url="login")
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context ={
        'income':income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request,"income/index.html",context)

@login_required(login_url="login")
def add_income(request):
    sources = Source.objects.all()
    context={
        'sources':sources,
        'values':request.POST
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']

        if not amount:
            messages.error(request, 'Amount is Required')
            return render(request,"income/add_income.html",context)
        if not description:
            messages.error(request, 'Description is Required')
            return render(request,"income/add_income.html",context)
        if not date:
            messages.error(request, 'Please select income date')
            return render(request,"income/add_income.html",context)
        
        UserIncome.objects.create(owner=request.user,amount=amount,description=description,source=source,date=date)
        messages.success(request, 'Record Save Successfully')
        return redirect('income')
    return render(request,"income/add_income.html",context)

# def expense_edit(request,id):
#     expense = UserIncome.objects.get(pk=id,owner=request.user)
#     categories = Source.objects.all()
#     context = {
#         'expense':expense,
#         'values': expense,
#         'categories':categories,
#     }
#     if request.method == 'POST':
#         amount = request.POST['amount']
#         description = request.POST['description']
#         category = request.POST['category']
#         date = request.POST['expense_date']

#         if not amount:
#             messages.error(request, 'Amount is Required')
#             return render(request,"expenses/edit-expense.html",context)
#         if not description:
#             messages.error(request, 'Description is Required')
#             return render(request,"expenses/edit-expense.html",context)
#         if not date:
#             messages.error(request, 'Please select expense date')
#             return render(request,"expenses/edit-expense.html",context)
        
#         expense.owner=request.user
#         expense.amount=amount
#         expense.description=description
#         expense.category=category
#         expense.date=date
#         expense.save()
#         messages.success(request, 'Expense Update Successfully')
#         return redirect('expences')
#     return render(request, 'expenses/edit-expense.html',context)

# def delete_expense(request,id):
#     expense = UserIncome.objects.get(pk=id,owner=request.user)
#     expense.delete()
#     messages.success(request, 'Expense Removed')
#     return redirect('expences')
