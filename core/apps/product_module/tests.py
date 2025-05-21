from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Product
from core.utils.constant import MANAGER, USER

# Create your tests here.

class ProductModelTest(TestCase):
    def setUp(self):
        self.product_data = {
            'name': 'Test Product',
            'barcode': '1234567890123',
            'price': 99.99,
            'stock': 100
        }
        self.product = Product.objects.create(**self.product_data)

    def test_product_creation(self):
        """Test if product is created correctly"""
        self.assertEqual(self.product.name, self.product_data['name'])
        self.assertEqual(self.product.barcode, self.product_data['barcode'])
        self.assertEqual(float(self.product.price), self.product_data['price'])
        self.assertEqual(self.product.stock, self.product_data['stock'])

    def test_product_str_method(self):
        """Test the string representation of the product"""
        self.assertEqual(str(self.product), self.product_data['name'])

    def test_product_meta(self):
        """Test product meta options"""
        self.assertEqual(Product._meta.db_table, 'products')
        self.assertEqual(Product._meta.verbose_name, 'Product')
        self.assertEqual(Product._meta.verbose_name_plural, 'Products')

class ProductIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test user with manager role
        self.manager_user = User.objects.create_user(
            username='manager',
            password='manager123'
        )
        self.manager_group = Group.objects.create(name='Manager')
        self.manager_user.groups.add(self.manager_group)
        
        # Create test user with regular user role
        self.regular_user = User.objects.create_user(
            username='user',
            password='user123'
        )
        self.user_group = Group.objects.create(name='User')
        self.regular_user.groups.add(self.user_group)

        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            barcode='1234567890123',
            price=99.99,
            stock=100
        )

    def test_product_list_view(self):
        """Test the product list view"""
        # Test as manager
        self.client.login(username='manager', password='manager123')
        response = self.client.get(reverse('product-module'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')
        self.assertContains(response, self.product.name)

        # Test as regular user
        self.client.login(username='user', password='user123')
        response = self.client.get(reverse('product-module'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')

    def test_product_create_view(self):
        """Test product creation"""
        self.client.login(username='manager', password='manager123')
        response = self.client.post(reverse('product-create'), {
            'name': 'New Product',
            'price': 149.99,
            'stock': 50
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_product_update_view(self):
        """Test product update"""
        self.client.login(username='manager', password='manager123')
        response = self.client.post(
            reverse('product-update', kwargs={'pk': self.product.pk}),
            {
                'name': 'Updated Product',
                'price': 199.99,
                'stock': 75
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(float(self.product.price), 199.99)
        self.assertEqual(self.product.stock, 75)

class ProductFunctionalTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.manager_user = User.objects.create_user(
            username='manager',
            password='manager123'
        )
        self.manager_group = Group.objects.create(name='Manager')
        self.manager_user.groups.add(self.manager_group)
        self.client.login(username='manager', password='manager123')

    def test_complete_product_workflow(self):
        """Test the complete product management workflow"""
        # 1. Create a product
        response = self.client.post(reverse('product-create'), {
            'name': 'Workflow Product',
            'price': 299.99,
            'stock': 100
        })
        self.assertEqual(response.status_code, 302)
        product = Product.objects.get(name='Workflow Product')
        self.assertIsNotNone(product.barcode)  # Verify barcode was generated

        # 2. Update the product
        response = self.client.post(
            reverse('product-update', kwargs={'pk': product.pk}),
            {
                'name': 'Updated Workflow Product',
                'price': 399.99,
                'stock': 150
            }
        )
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Updated Workflow Product')
        self.assertEqual(float(product.price), 399.99)
        self.assertEqual(product.stock, 150)

        # 3. Delete the product
        response = self.client.post(reverse('product-delete', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())

    def test_unauthorized_access(self):
        """Test unauthorized access to product management"""
        # Create a regular user
        regular_user = User.objects.create_user(
            username='user',
            password='user123'
        )
        user_group = Group.objects.create(name='User')
        regular_user.groups.add(user_group)

        # Create a product
        product = Product.objects.create(
            name='Test Product',
            barcode='1234567890123',
            price=99.99,
            stock=100
        )

        # Test as regular user
        self.client.login(username='user', password='user123')
        
        # Try to access create view
        response = self.client.get(reverse('product-create'))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Try to access update view
        response = self.client.get(reverse('product-update', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Try to access delete view
        response = self.client.get(reverse('product-delete', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden
