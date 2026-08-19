from wsgiref.validate import validator

from django import forms
from django.core import validators
from django.forms import ModelForm
from django.contrib.auth.models import Group

from .models import Product, Order


class ProductForm(ModelForm):
    # images = forms.FileField(
    #     required=False,
    # )

    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'description',
            'discount',
            'preview',
        )


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = 'user','delivery_address', 'promocode', 'products'


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = 'name',


class OrderImportForm(forms.Form):
    file = forms.FileField()