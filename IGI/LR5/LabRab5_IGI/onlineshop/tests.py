from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from django.test import TestCase
from .models import Employee, Client, Product, Order
from django.test import TestCase
from django.utils import timezone
from onlineshop.views import get_user_time


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='john', password='doe')
        Group.objects.create(name='Employees')
        Employee.objects.create(user=user, first_name='John', last_name='Doe', position='Manager')

    def test_first_name_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_first_name_max_length(self):
        employee = Employee.objects.get(id=1)
        max_length = employee._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        employee = Employee.objects.get(id=1)
        max_length = employee._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='jane', password='doe')
        Group.objects.create(name='Shop Members')
        Client.objects.create(user=user, first_name='Jane', last_name='Doe')

    def test_first_name_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        product_type = ProductType.objects.create(name='Test Type')
        Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                               product_type=product_type)

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='jane', password='doe')
        Group.objects.create(name='Shop Members')
        client = Client.objects.create(user=user, first_name='Jane', last_name='Doe')
        product_type = ProductType.objects.create(name='Test Type')
        product = Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                                         product_type=product_type)
        product_instance = ProductInstance.objects.create(product=product, quantity=1)
        cls.order = Order.objects.create(client=client, total_price=10.00)
        cls.order.products.add(product_instance)

    def test_total_price_label(self):
        field_label = self.order._meta.get_field('total_price').verbose_name
        self.assertEqual(field_label, 'total price')

    def test_total_price_value(self):
        self.assertEqual(self.order.total_price, 10.00)


class ProductTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProductType.objects.create(name='Test Type')

    def test_name_label(self):
        product_type = ProductType.objects.get(id=1)
        field_label = product_type._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        product_type = ProductType.objects.get(id=1)
        max_length = product_type._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_str_method(self):
        product_type = ProductType.objects.get(id=1)
        expected_object_name = product_type.name
        self.assertEqual(str(product_type), expected_object_name)


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name='Test Manufacturer', address='Test Address', phone='1234567890')

    def test_name_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_str_method(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = manufacturer.name
        self.assertEqual(str(manufacturer), expected_object_name)


class ProductInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        product_type = ProductType.objects.create(name='Test Type')
        product = Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                                         product_type=product_type)
        cls.product_instance = ProductInstance.objects.create(product=product, quantity=2)

    def test_total_price(self):
        expected_total_price = self.product_instance.product.price * self.product_instance.quantity
        self.assertEqual(self.product_instance.total_price, expected_total_price)

    def test_str_method(self):
        expected_object_name = f'{self.product_instance.id} ({self.product_instance.product.name})'
        self.assertEqual(str(self.product_instance), expected_object_name)

class PickupLocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PickupLocation.objects.create(name='Test Location', address='Test Address')

    def test_str_method(self):
        pickup_location = PickupLocation.objects.get(id=1)
        expected_object_name = pickup_location.name
        self.assertEqual(str(pickup_location), expected_object_name)


class PromoCodeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PromoCode.objects.create(code='TESTCODE', discount=10.00)

    def test_str_method(self):
        promo_code = PromoCode.objects.get(id=1)
        expected_object_name = promo_code.code
        self.assertEqual(str(promo_code), expected_object_name)


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='jane', password='doe')
        Review.objects.create(user=user, rating=5, text='Great product!')

    def test_text_content(self):
        review = Review.objects.get(id=1)
        expected_text = 'Great product!'
        self.assertEqual(review.text, expected_text)


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Article.objects.create(title='Test Article', summary='Test Summary', content='Test Content')

    def test_str_method(self):
        article = Article.objects.get(id=1)
        expected_object_name = article.title
        self.assertEqual(str(article), expected_object_name)


class CompanyInfoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CompanyInfo.objects.create(text='Test Text', history='Test History', details='Test Details')

    def test_str_method(self):
        company_info = CompanyInfo.objects.get(id=1)
        expected_object_name = 'Company Information'
        self.assertEqual(str(company_info), expected_object_name)


    def test_text_content(self):
        company_info = CompanyInfo.objects.get(id=1)
        expected_text = 'Test Text'
        self.assertEqual(company_info.text, expected_text)


class FAQModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        FAQ.objects.create(question='Test Question', answer='Test Answer')

    def test_str_method(self):
        faq = FAQ.objects.get(id=1)
        expected_object_name = faq.question
        self.assertEqual(str(faq), expected_object_name)

    def test_question_text(self):
        faq = FAQ.objects.get(id=1)
        expected_text = 'Test Question'
        self.assertEqual(faq.question, expected_text)

    def test_answer_text(self):
        faq = FAQ.objects.get(id=1)
        expected_text = 'Test Answer'
        self.assertEqual(faq.answer, expected_text)


class JobModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Job.objects.create(title='Test Job', description='Test Description')

    def test_str_method(self):
        job = Job.objects.get(id=1)
        expected_object_name = job.title
        self.assertEqual(str(job), expected_object_name)

    def test_description_text(self):
        job = Job.objects.get(id=1)
        expected_text = 'Test Description'
        self.assertEqual(job.description, expected_text)


class GetUserTimeTest(TestCase):
    def test_get_user_time(self):
        user_time_data = get_user_time()
        current_time = timezone.localtime(timezone.now())

        self.assertIn("user_timezone", user_time_data)
        self.assertIn("current_date_formatted", user_time_data)
        self.assertIn("calendar_text", user_time_data)

        self.assertEqual(user_time_data["user_timezone"], str(timezone.get_current_timezone()))
        self.assertEqual(user_time_data["current_date_formatted"], current_time.strftime("%d.%m.%Y %H:%M:%S"))
        self.assertEqual(user_time_data["calendar_text"], current_time.strftime("%B %Y"))

from onlineshop.models import Product, Client, Cart, ProductInstance

from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from onlineshop.models import Product, Client, Cart, ProductInstance

class AddToCartTest(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product_type = ProductType.objects.create(name='Test Type')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                                              product_type=self.product_type)
        Group.objects.create(name='Shop Members')
        self.client_object = Client.objects.create(user=self.user)
        self.cart = Cart.objects.create(client=self.client_object)

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Check that redirect happened
        self.cart.refresh_from_db()  # Refresh the cart object from the database
        product_in_cart = self.cart.products.filter(product__name=self.product.name).first()
        self.assertIsNotNone(product_in_cart)  # Check that the product was added to the cart
        self.assertEqual(product_in_cart.quantity, 1)  # Check that the quantity of the product is correct


from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User, Group
from onlineshop.models import Product, Client, Cart, ProductInstance, ProductType

class CartUpdateTest(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product_type = ProductType.objects.create(name='Test Type')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                                              product_type=self.product_type)
        Group.objects.create(name='Shop Members')
        self.client_object = Client.objects.create(user=self.user)
        self.cart = Cart.objects.create(client=self.client_object)
        self.product_instance = ProductInstance.objects.create(product=self.product, customer=self.client_object, quantity=1)
        self.cart.products.add(self.product_instance)


from unittest import TestCase
from unittest.mock import patch
from onlineshop.views import get_cat_fact

class GetCatFactTest(TestCase):
    @patch('onlineshop.views.requests.get')
    def test_get_cat_fact(self, mock_get):
        # Создаем фиктивный ответ от API
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'fact': 'Cats are cute.'}

        response = get_cat_fact()

        self.assertEqual(response, {'fact': 'Cats are cute.'})
        mock_get.assert_called_once_with('https://catfact.ninja/fact')

