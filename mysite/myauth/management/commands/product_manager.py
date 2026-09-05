from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name= 'product_manager',
        )
        permission_product = Permission.objects.get(
            codename = 'add_product',
        )
        # добавление разрешения в группу
        group.permissions.add(permission_product)
        group.save()
