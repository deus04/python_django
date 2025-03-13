from timeit import default_timer

import requests
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order


class ShopIndexView(View):
    def get(self, request: HttpRequest)-> HttpResponse:
        products = [
            ("Laptop", 1999),
            ("Dasktop", 2999),
            ("Smartphone", 999),
        ]
        context = {
            'time_running': default_timer(),
            "products": products
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest)-> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self,requests: HttpRequest):
        form = GroupForm(requests.POST)
        if form.is_valid():
            form.save()
        return redirect(requests.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = 'product'


class ProductsListView(ListView):
    template_name = 'shopapp/product-list.html'
    #odel = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        #return self.request.user.groups.filter(name='secret-group').exists()
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.created_by=self.request.user
        return super().form_valid(form)

    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products-list')
    template_name = 'shopapp/product_create.html'


class ProductUpdateView(UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product-details',
            kwargs={'pk':self.object.pk}
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products-list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/orders-list.html'
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )
    context_object_name = 'orders'


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user','delivery_address', 'promocode', 'products'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order-details',
            kwargs={'pk':self.object.pk}
        )


class OrderCreateView(CreateView):
    model = Order
    fields = 'user','delivery_address', 'promocode', 'products'
    success_url = reverse_lazy('shopapp:orders-list')
    template_name = 'shopapp/order_create.html'


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders-list')

    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     self.object.archived = True
    #     self.object.save()
    #     return HttpResponseRedirect(success_url)