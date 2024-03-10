from django.shortcuts import render

# Create your views here.

def preferences(request):
    return render(request, 'preferences/index.html')