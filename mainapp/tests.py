from django.test import TestCase
from django.test.client import Client
from mainapp.models import Products, Category
from django.core.management import call_command
from mainapp.views import products
from authapp.models import Users


class TestMainappSmoke(TestCase):
    fixtures = ['mainapp.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/page/2/')
        self.assertEqual(response.status_code, 200)


class TestUserManagement(TestCase):
    fixtures = ['mainapp.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = Users.objects.create_user('georg', \
                                              'georg@geekshop.ru', 'geekbrains')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'GeekShop Store')
        self.assertNotContains(response, 'Пользователь', status_code=200)

        # данные пользователя
        self.client.login(username='georg', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        print(response)
        self.assertContains(response, 'Georg', status_code=200)
        self.assertEqual(response.context['user'], self.user)



class ProductsTestCase(TestCase):
   def setUp(self):
       category = Category.objects.create(name='Худи',
                                          description='описание')

       self.product_1 = Products.objects.create(name = 'Худи_1',
                                                description = 'описание продукта_1',
                                                short_description = 'короткое_описание продукта_1',
                                                price = 1234,
                                                quantity = 56,
                                                category = category)

   def test_product_get(self):
       product_1 = Products.objects.get(name='Худи_1')
       self.assertEqual(product_1, self.product_1)

   def test_product_print(self):
       product_1 = Products.objects.get(name='Худи_1')
       self.assertEqual(str(product_1), 'Худи_1')
