from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse

# Create your views here.

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumaric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry, username already taken, choose another one.'},status=409)
        return JsonResponse({'username_valid':True})

class RegistrationView(View):
    def get(self,request):
        return render(request, 'authentication/register.html')
