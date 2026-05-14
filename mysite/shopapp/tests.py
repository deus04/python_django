from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2,3)
        self.assertEqual(result,5)


class ProductCreateViewTestCase(TestCase):  #TODO не срабатывают тесты
    def setUp(self):
        # Создаем суперпользователя, так как ProductCreateView требует is_superuser
        self.user = User.objects.create_superuser(
            username="testuser",
            password="password",
            email="test@test.com"
        )
        # Логинимся перед выполнением запросов
        self.client.force_login(self.user)

    def test_create_product(self):
        response = self.client.post(
            reverse('shopapp:product-create'),  # Исправляем опечатку в маршруте
            {
                'name':'Table',
                'price':'123.45',
                'description':'A good table',
                'discount':'10',
                   }
        )
        self.assertRedirects(response, reverse('shopapp:products-list'))
