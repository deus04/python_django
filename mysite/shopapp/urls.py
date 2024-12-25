from django.contrib import admin
from django.urls import path

from .views import shop_index, groups_list, products_list, orders_list


app_name = 'shopapp'
urlpatterns = [
    path('', shop_index, name='index'),
    path('groups/', groups_list, name='groups-list'),
    path('products/', products_list, name='products-list'),
    path('orders/', orders_list, name='orders-list'),

]
