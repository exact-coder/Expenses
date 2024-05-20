from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from userincome.models import Source,UserIncome
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

# Create your views here.


def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        incomes = UserIncome.objects.filter(amount__startswith=search_str,owner=request.user) | UserIncome.objects.filter(date__startswith=search_str,owner=request.user) | UserIncome.objects.filter(source__icontains=search_str,owner=request.user) | UserIncome.objects.filter(description__icontains=search_str,owner=request.user)
        data = incomes.values()
        return JsonResponse(list(data),safe=False)



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

def income_edit(request,id):
    income = UserIncome.objects.get(pk=id,owner=request.user)
    sources = Source.objects.all()
    context = {
        'income':income,
        'values': income,
        'sources':sources,
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']

        if not amount:
            messages.error(request, 'Amount is Required')
            return render(request,"income/edit-income.html",context)
        if not description:
            messages.error(request, 'Description is Required')
            return render(request,"income/edit-income.html",context)
        if not date:
            messages.error(request, 'Please select income date')
            return render(request,"income/edit-income.html",context)
        
        income.owner=request.user
        income.amount=amount
        income.description=description
        income.source=source
        income.date=date
        income.save()
        messages.success(request, 'Record Update Successfully')
        return redirect('income')
    return render(request, 'income/edit-income.html',context)

def delete_income(request,id):
    income = UserIncome.objects.get(pk=id,owner=request.user)
    income.delete()
    messages.success(request, 'Record Removed')
    return redirect('income')


