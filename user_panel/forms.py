from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from user_app.models import User


class EditInfoModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'avatar'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام شما"}),
            'last_name': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ایمیل شما"}),
            'avatar': forms.FileInput(attrs={
                "class": "form-control",
                "placeholder": "تصویر پروفایل",
            }),
        }

        labels = {
            'first_name': "نام",
            'last_name': "نام خانوادگی",
            'avatar': "تصویر پروفایل",

        }
        error_messages = {
            'first_name': {
                'required': 'لطفا نام خود را وارد کنید',
                'max_length': 'تعداد حروف نام شما بیشتر از حد مجاز است'
            },
            'last_name': {
                'required': 'لطفا نام خانوادگی خود را وارد کنید',
            }
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="رمز عبور فعلی",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور فعلی"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100)
        ],
    )
    password = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور جدید"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100)
        ],
    )
    confirm_password = forms.CharField(
        label="تکرار رمز عبور جدید",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "تکرار رمز عبور جدید"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100)
        ],
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('رمز عبور و تکرار رمز عبور مغایرت ندارد')
