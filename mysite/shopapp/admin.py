import csv
import io
from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin

from shopapp.forms import OrderImportForm


class OrderInline(admin.TabularInline):
    model = Product.orders.through


class ProductInLine(admin.StackedInline):
    model = ProductImage


@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
        ProductInLine,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = '-name', "pk"
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse'),
        }),
        ('Images', {
            'fields': ('preview',),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archived" is for soft delete'
        })

    ]

    def description_short(self, obj: Product):
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'

#admin.site.register(Product, ProductAdmin)


# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changelist.html"

    inlines = [
        ProductInline,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.import_csv),
                name="shopapp_order_import",
            ),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "GET":
            form = OrderImportForm()
            return render(
                request,
                "shopapp/csv_form.html",
                {"form": form},
            )

        form = OrderImportForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data["file"]

            decoded_file = file.read().decode("utf-8")
            reader = csv.DictReader(io.StringIO(decoded_file))

            for row in reader:
                user = User.objects.get(username=row["user"])

                order = Order.objects.create(
                    delivery_address=row["delivery_address"],
                    promocode=row["promocode"],
                    user=user,
                )

                product_ids = row["products"].split(";")
                products = Product.objects.filter(id__in=product_ids)

                order.products.set(products)

            return redirect("admin:shopapp_order_changelist")

        return render(
            request,
            "shopapp/csv_form.html",
            {"form": form},
        )

