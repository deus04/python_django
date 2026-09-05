from django.contrib import admin

from .models import Author, Category, Tag, Article


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)