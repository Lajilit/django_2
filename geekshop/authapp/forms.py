import hashlib
import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import BooleanField

from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    error_messages = {
        'invalid_login': (
            "Пожалуйста, введите правильныые имя пользователя и пароль. \
            Учтите что оба поля могут быть чувствительны к регистру."
        ),
        'inactive': (
            "Этот аккаунт неактивен. Для активации перейдите по ссылке, \
            высланной вам на электронную почту."
        ),
    }


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2',
                  'email',
                  # 'age',
                  'avatar',
                  'is_staff'
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    # def clean_age(self):
    #     data = self.cleaned_data['age']
    #     if data < 18:
    #         raise forms.ValidationError("Вы слишком молоды!")
    #
    #     return data

    def save(self, **kwargs):
        user = super(ShopUserRegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1(
            (user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            # 'age',
            'avatar',
            'password',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    # def clean_age(self):
    #     data = self.cleaned_data['age']
    #     if data < 18:
    #         raise forms.ValidationError("Вы слишком молоды!")
    #
    #     return data
