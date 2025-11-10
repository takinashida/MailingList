from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User

class VisualMixin:

    def form_control(self, field, placeholder):
        return self.fields[field].widget.attrs.update({
            "class": "form-control",
            placeholder: "Введите свой email:"
        })

class UserRegisterForm(UserCreationForm, VisualMixin):
    class Meta:
        model=User
        fields=["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.form_control("email", "Введите email:")
        self.form_control("username", "Введите свое имя:")
        self.form_control("password1", "Введите пароль:")
        self.form_control("password2", "Повторите пароль:")

class UserAuthForm(forms.ModelForm, VisualMixin):
    class Meta:
        model = User
        fields = ["username","password"]

    def __init__(self, *args, **kwargs):
        super(UserAuthForm, self).__init__(*args, **kwargs)

        self.form_control("username", "Введите свое имя:")
        self.form_control("password", "Введите пароль:")

class UserChangeForm(UserCreationForm, VisualMixin):
    class Meta:
        model=User
        fields=["username", "email"]

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        self.form_control("email", "Введите email:")
        self.form_control("username", "Введите свое имя:")
