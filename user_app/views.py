from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from .forms import RegisterForm, LoginForm
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


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            "login_form": login_form
        }

        return render(request, 'user_app/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user_email = login_form.cleaned_data.get("email")
            user_password = login_form.cleaned_data.get("password")
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error(field="email", error="حساب کاربری شما فعال نشده است")

                else:
                    is_correct_password = user.check_password(user_password)
                    if is_correct_password:
                        login(request, user)
                        return redirect(reverse("todo-list"))
                    else:
                        login_form.add_error(field="email", error="کاربری با مشخصات شما یافت نشد")
            else:
                login_form.add_error(field="email", error="کاربری با مشخصات شما یافت نشد")

        context = {
            "login_form": login_form
        }

        return render(request, "user_app/login.html", context)
