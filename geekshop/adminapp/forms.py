from django import forms
from django.forms import BooleanField

from authapp.forms import ShopUserEditForm, ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            # 'age',
            'avatar',
            'is_active',
            'is_staff',
            'is_deleted'
        )


class ShopUserAdminRegisterForm(ShopUserRegisterForm):
    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'email',
            # 'age',
            'avatar',
            'is_active',
            'is_staff',
            'is_deleted',
        )


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        # fields = (
        #     'name',
        #     'description',
        # )
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = (
        #     'category',
        #     'name',
        #     'image',
        #     'short_desc',
        #     'description',
        #     'price',
        #     'quantity',
        # )
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
