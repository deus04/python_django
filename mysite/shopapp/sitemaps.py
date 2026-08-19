from django.contrib.sitemaps import Sitemap

from .models import Product


class ShopSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Product.objects.all()