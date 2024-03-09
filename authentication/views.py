from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from authentication.utils import token_generator

# Create your views here.
# JavaScript username validition check 
class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumaric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry, username already taken, choose another one.'},status=409)
        return JsonResponse({'username_valid':True})

# JavaScript email validition check 
class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Invalid Email'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'sorry, email already use, choose another one.'},status=409)
        return JsonResponse({'email_valid':True})

class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')

class RegistrationView(View):
    def get(self,request):
        return render(request, 'authentication/register.html')
    
    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues':request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 4:
                    messages.error(request, "Password too short")
                    return render(request, 'authentication/register.html',context)
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                uidb64= urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                activate_url='http://'+domain+link

                email_subject = "Activate Your Account"
                email_body = 'Hi ,' + user.username + '\n Please use this link to verify your account\n' + activate_url
                email_send = EmailMessage(
                    email_subject,
                    email_body,
                    'exactcoder0@gmail.com',
                    [email]
                )
                email_send.send(fail_silently=False)
                messages.success(request, "User Created Successfully")
                return render(request, 'authentication/register.html')
        
        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        return redirect('login')


