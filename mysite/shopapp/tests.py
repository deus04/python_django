from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from django.test import Client

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2,3)
        self.assertEqual(result,5)


class ProductCreateViewTestCase(TestCase):  #TODO не срабатывают тесты
    def setUp(self):
        self.product_name = ''.join(choices(ascii_letters,k=10))
        Product.objects.filter(name=self.product_name).delete()
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
                'name':self.product_name,
                'price':'123.45',
                'description':'A good table',
                'discount':'10',
                   }
        )
        self.assertRedirects(response, reverse('shopapp:products-list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.user = User.objects.create_superuser(
            username="testuser",
            password="password",
            email="test@test.com"
        )
        # Логинимся перед выполнением запросов
        cls.client.force_login(cls.user)

        cls.product = Product.objects.create(
            name="Best product",
            created_by=cls.user
        )

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product-details', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product-details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:products-list"))
        products = Product.objects.filter(archived=False).all()
        products_ = response.context['products']
        self.assertQuerySetEqual(
            qs=products,
            values=(p.pk for p in products_),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/product-list.html')


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='123'
        )

    def test_orders_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('shopapp:orders-list'))
        self.assertContains(response, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders-list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse('shopapp:products-export')
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk':product.pk,
                'name':product.name,
                'price':str(product.price),
                'archived':product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data
        )


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='123',
        )

        permission = Permission.objects.get(
            codename='view_order'
        )

        cls.user.user_permissions.add(permission)

    def setUp(self):
        self.client.force_login(self.user)

        self.product = Product.objects.create(
            name='Phone',
            price=100,
            created_by=self.user,
        )

        self.order = Order.objects.create(
            delivery_address='Moscow',
            promocode='TESTCODE',
            user=self.user,
        )

        self.order.products.add(self.product)

    def tearDown(self):
        self.order.delete()


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse(
                "shopapp:order-details",
                kwargs={"pk": self.order.pk}
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            self.order.delivery_address
        )

        self.assertContains(
            response,
            self.order.promocode
        )

        self.assertEqual(
            response.context["order"].pk,
            self.order.pk
        )

class OrdersExportTestCase(TestCase):
    fixtures = [
        'orders-data.json',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='staff_user',
            password='123',
            is_staff=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        #super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_export(self):
        response = self.client.get(
            reverse("shopapp:orders-export")
        )

        self.assertEqual(response.status_code, 200)