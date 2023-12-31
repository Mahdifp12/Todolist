from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
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
                register_form.add_error('email', 'ایمیل وارد شده تکراری میباشد...لطفا وارد شوید')

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
                return redirect(reverse('login-user-page'))
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


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # Todo: show success message to user
                return redirect(reverse('login-user-page'))

            else:
                pass
                # Todo: show your account was activated message to user

        raise Http404

    def post(self, request):
        pass


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgetPasswordForm()
        context = {
            "form": forget_pass_form
        }
        return render(request, 'user_app/forgot_password.html', context)

    def post(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm(request.POST)

        if forget_password_form.is_valid():
            user_email = forget_password_form.cleaned_data.get("email")
            user: User = User.objects.filter(email__iexact=user_email).first()

            if user is not None:
                send_email('بازیابی رمز عبور', user.email, {"user": user}, "emails/forget_password_activate.html")
                return redirect(reverse("login-user-page"))

        context = {
            "form": forget_password_form
        }

        return render(request, 'user_app/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse("login-page"))

        reset_password_form = ResetPasswordForm()

        context = {
            "form": reset_password_form,
            "user": user
        }
        return render(request, 'user_app/reset_password.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()

        if reset_password_form.is_valid():
            if user is None:
                return redirect(reverse("login-page"))

            user_new_pass = reset_password_form.cleaned_data.get("password")  # Get password from user form
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()

            return redirect(reverse("login-page"))

        context = {
            "form": reset_password_form,
            "user": user
        }
        return render(request, 'user_app/reset_password.html', context)


class LogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect(reverse("login-user-page"))
