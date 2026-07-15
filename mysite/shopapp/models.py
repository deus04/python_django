from django.contrib.auth.models import User
from django.db import models
from myauth.models import Profile


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    pk = instance.pk or 'new'
    filename = filename
    return f'products/product_{pk}/preview/{filename}'

class Product(models.Model):
    '''
    Модель Product представляет товар, который можно продавать в магазине

    Заказы тут: :model:`shopapp.Orderсв`
    '''
    class Meta:
        ordering = ['name', 'price']

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_ad = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    @property
    def description_short(self):
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + '...'

    def __str__(self):
        return f'Product(pk={self.pk}, name={self.name!r})'


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    pk = instance.product.pk or 'new'
    filename = filename
    return f'products/product_{pk}/images/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
    receipt = models.FileField(null=True, upload_to='orders/receipts/')
