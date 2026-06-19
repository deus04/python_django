from timeit import default_timer

import requests
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        'name',
        'description',
    ]
    filterset_fields = [
        'name',
        'price',
        'description',
        'discount',
        'archived',
    ]
    ordering_fields = [
        'name',
        'price',
        'discount',
        'created_ad'
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_fields = [
        'user',
        'promocode',
    ]

    ordering_fields = [
        'created_at',
    ]


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
    # model = Product
    queryset = Product.objects.prefetch_related('images')
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
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products-list')
    template_name = 'shopapp/product_create.html'


class ProductUpdateView(UpdateView):
    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = '_update_form'
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            'shopapp:product-details',
            kwargs={'pk':self.object.pk}
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


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


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'archived': product.archived,
            }
            for product in products
        ]
        return JsonResponse({'products': products_data})


class OrdersExportView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user_id,
                'products': [
                    product.pk for product in order.products.all()
                ],
            }
            for order in orders
        ]

        return JsonResponse({'orders': orders_data})