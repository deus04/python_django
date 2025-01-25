from wsgiref.validate import validator

from django import forms
from django.core import validators

from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", 'price', 'discount', 'description'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'user','delivery_address', 'promocode', 'products'
