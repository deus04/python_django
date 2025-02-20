from wsgiref.validate import validator

from django.core import validators
from django.forms import ModelForm
from django.contrib.auth.models import Group

from .models import Product, Order


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "name", 'price', 'discount', 'description'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = 'user','delivery_address', 'promocode', 'products'


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = 'name',