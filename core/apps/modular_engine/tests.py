from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Module
from django.contrib import messages
from django.core.management import call_command

# Create your tests here.

class ModuleModelTest(TestCase):
    def setUp(self):
        self.module_data = {
            'name': 'Test Module',
            'slug': 'test-module',
            'description': 'This is a test module',
            'is_active': True,
            'version': 1.0
        }
        self.module = Module.objects.create(**self.module_data)

    def test_module_creation(self):
        """Test if module is created correctly"""
        self.assertEqual(self.module.name, self.module_data['name'])
        self.assertEqual(self.module.slug, self.module_data['slug'])
        self.assertEqual(self.module.description, self.module_data['description'])
        self.assertEqual(self.module.is_active, self.module_data['is_active'])
        self.assertEqual(float(self.module.version), self.module_data['version'])

    def test_module_str_method(self):
        """Test the string representation of the module"""
        self.assertEqual(str(self.module), self.module_data['name'])

    def test_module_meta(self):
        """Test module meta options"""
        self.assertEqual(Module._meta.db_table, 'modules')
        self.assertEqual(Module._meta.verbose_name, 'Module')
        self.assertEqual(Module._meta.verbose_name_plural, 'Modules')

class ModuleIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.group = Group.objects.create(name='TestGroup')
        self.user.groups.add(self.group)
        self.client.login(username='testuser', password='testpass123')
        
        # Create a test module
        self.module = Module.objects.create(
            name='Test Module',
            slug='test-module',
            description='Test Description',
            is_active=True,
            version=1.0
        )

    def test_module_list_view(self):
        """Test the module list view"""
        response = self.client.get(reverse('modular-tools'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'module_list.html')
        self.assertContains(response, self.module.name)

    def test_module_install_action(self):
        """Test module installation"""
        response = self.client.post(
            reverse('module-action', kwargs={'slug': self.module.slug, 'action': 'install'})
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.module.refresh_from_db()
        self.assertTrue(self.module.is_active)

    def test_module_uninstall_action(self):
        """Test module uninstallation"""
        response = self.client.post(
            reverse('module-action', kwargs={'slug': self.module.slug, 'action': 'uninstall'})
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.module.refresh_from_db()
        self.assertFalse(self.module.is_active)

class ModuleFunctionalTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.group = Group.objects.create(name='TestGroup')
        self.user.groups.add(self.group)
        self.client.login(username='testuser', password='testpass123')

    def test_signup_flow(self):
        """Test the complete signup flow"""
        # Test signup form
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

        # Test signup submission
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'group': self.group.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_user = User.objects.get(username='newuser')
        self.assertTrue(new_user.groups.filter(id=self.group.id).exists())

    def test_module_upgrade_flow(self):
        """Test the complete module upgrade flow"""
        # Create a module with an older version
        module = Module.objects.create(
            name='Test Module',
            slug='test-module',
            description='Test Description',
            is_active=True,
            version=1.0
        )

        # Test upgrade action
        response = self.client.post(
            reverse('module-action', kwargs={'slug': module.slug, 'action': 'upgrade'})
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Verify module was upgraded
        module.refresh_from_db()
        self.assertEqual(float(module.version), 1.0)  # Version should be updated
