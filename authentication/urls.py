from django.urls import path
from .views import RegistrationView,UsernameValidationView,EmailValidationView,LoginView,VerificationView,LogoutView,RequestPasswordResetEmail
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("register",RegistrationView.as_view(),name="register"),
    path("login",LoginView.as_view(),name="login"),
    path("logout",LogoutView.as_view(),name="logout"),
    path("request-reset-link",RequestPasswordResetEmail.as_view(),name="request-password"),
    path("activate/<uidb64>/<token>",VerificationView.as_view(),name="activate"),
    path("validate-username",csrf_exempt(UsernameValidationView.as_view()),name="validate-username"),
    path("validate-email",csrf_exempt(EmailValidationView.as_view()),name="validate-email"),
]
