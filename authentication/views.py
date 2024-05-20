from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from authentication.utils import account_activation_token
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):

        self.email.send(fail_silently=False)
        


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
        
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request, 'Welcome '+ user.get_username() + ', you are logged in')
                    return redirect('expences')
                messages.error(request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid credentials, try again!!')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Invalid credentials, try again!!')
        return render(request, 'authentication/login.html')
    
class LogoutView(View):
    def get(self,request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')

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
                link=reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(user)})
                activate_url='http://'+domain+link

                email_subject = "Activate Your Account"
                email_body = 'Hi ,' + user.username + '\n Please use this link to verify your account\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'exactcoder0@gmail.com',
                    [email]
                )
                EmailThread(email).start()
                messages.success(request, "User Created Successfully")
                return render(request, 'authentication/register.html')
        
        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):

        try:
            id= force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not account_activation_token.check_token(user,token):
                return redirect('login'+'?message'+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active=True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as e:
            pass
        return redirect('login')

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    def post(self, request):
        email = request.POST['email']
        context ={
            'values': request.POST,
        }

        if not validate_email(email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'authentication/reset-password.html',context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
        


        if user.exists():
            email_contents = {
                'user':user[0],
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }
            link=reverse('reset-user-password',kwargs={'uidb64':email_contents['uid'],'token':email_contents['token']})
            email_subject = "Password Reset Instructions"
            reset_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                # Email Body
                f'Hi There, Please click the link below to reset your password \n {reset_url}',
                'exactcoder0@gmail.com',
                [email]
            )
            EmailThread(email).start()
        messages.success(request, 'We have send you an email to reset your password')
        
        return render(request, 'authentication/reset-password.html')

class CompletePasswordReset(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Password link is Invalid, Request for new one")
                return redirect('request-password')
        except Exception as e:
            pass
            return render(request, 'authentication/set-new-password.html',context)
        return render(request, 'authentication/set-new-password.html',context)
    
    def post(self,request,uidb64,token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords donot match')
            return render(request, 'authentication/set-new-password.html',context)
        if len(password) < 6:
            messages.error(request, "Password must be higher then 6 characters")
            return render(request, 'authentication/set-new-password.html',context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset Successfully")
            return redirect('login')
        except Exception as e:
            messages.info(request, "Something Wrong Happened!!")
            print(e)
            return render(request, 'authentication/set-new-password.html',context)

        
    

