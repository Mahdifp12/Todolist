from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from .forms import RegisterForm
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from utils.email_service import send_email


# Create your views here.

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            "register_form": register_form
        }

        return render(request, 'user_app/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user_email = register_form.cleaned_data.get("email")
            user_password = register_form.cleaned_data.get("password")
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری میباشد')

            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email
                )
                new_user.set_password(user_password)
                new_user.save()
                # todo: send email active code
                send_email('فعالسازی حساب کاربری', new_user.email, {"user": new_user}, "emails/activate_account.html")
                return redirect(reverse('login-page'))
        context = {
            "register_form": register_form
        }

        return render(request, 'user_app/register.html', context)
