from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class AddTodoForm(forms.Form):
    title = forms.CharField(
        label="عنوان",
        widget=forms.TextInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ],
    )
    description = forms.CharField(
        label="توضیحات",
        widget=forms.TextInput(),
        validators=[
            validators.MaxLengthValidator(200),
        ],
    )
