from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from vendor.models import Vendor, Category, Product

class VendorFlowsTest(TestCase):
    def setUp(self):
        self.username = 'vendoruser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.vendor = Vendor.objects.create(
            user=self.user,
            business_name='Biz',
            business_email='biz@example.com',
            phone_number='9999999999',
            business_address='Addr',
            city='City',
            state='State',
            postal_code='000000',
            gst_number='GST1234',
            bank_account='1234567890',
            bank_ifsc='IFSC',
            bank_name='Bank',
            status='approved'  # Approve vendor for testing
        )
        self.category = Category.objects.create(name='Test Cat')

    def test_vendor_registration_creates_pending_vendor(self):
        """Test that new vendor registration creates pending vendor"""
        resp = self.client.post(reverse('vendor_register'), {
            'username': 'newvendor',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(resp.status_code, 302)
        new_user = User.objects.get(username='newvendor')
        self.assertEqual(new_user.vendor_profile.status, 'pending')

    def test_pending_vendor_cannot_login(self):
        """Test that pending vendor cannot login"""
        # Create pending vendor
        pending_user = User.objects.create_user(username='pending', password='testpass123')
        Vendor.objects.create(
            user=pending_user,
            business_name='Pending Biz',
            business_email='pending@example.com',
            phone_number='9999999999',
            business_address='Addr',
            city='City',
            state='State',
            postal_code='000000',
            gst_number='GST5678',
            bank_account='1234567890',
            bank_ifsc='IFSC',
            bank_name='Bank',
            status='pending'
        )
        
        # Try to login
        resp = self.client.post(reverse('vendor_login'), {
            'username': 'pending',
            'password': 'testpass123'
        })
        # Should not login - redirect stays on login page
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.wsgi_request.user.is_authenticated)

    def test_approved_vendor_can_login(self):
        """Test that approved vendor can login"""
        resp = self.client.post(reverse('vendor_login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('vendor_dashboard'), resp.url)

    def test_vendor_logout_redirects_to_vendor_login(self):
        """Test logout redirects to vendor login"""
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse('vendor_logout'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('vendor_login'), resp.url)

    def test_approved_vendor_can_create_product(self):
        """Test approved vendor can create product"""
        self.client.login(username=self.username, password=self.password)
        url = reverse('product_create')
        data = {
            'name': 'Test Product',
            'description': 'Desc',
            'category': str(self.category.id),
            'price': '10.00',
            'discount_price': '',
            'stock': '5',
            'sku': 'SKU12345',
            'weight': '0.5',
            'dimensions': '10x10x10',
            'is_featured': ''
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Product.objects.filter(sku='SKU12345', vendor=self.vendor).exists())

    def test_dashboard_restricted_to_approved_vendors(self):
        """Test that dashboard is restricted to approved vendors"""
        # Create pending vendor
        pending_user = User.objects.create_user(username='pending2', password='testpass123')
        pending_vendor = Vendor.objects.create(
            user=pending_user,
            business_name='Pending Biz 2',
            business_email='pending2@example.com',
            phone_number='9999999999',
            business_address='Addr',
            city='City',
            state='State',
            postal_code='000000',
            gst_number='GST9012',
            bank_account='1234567890',
            bank_ifsc='IFSC',
            bank_name='Bank',
            status='pending'
        )
        
        # Even if logged in as pending vendor, should redirect
        self.client.login(username='pending2', password='testpass123')
        resp = self.client.get(reverse('vendor_dashboard'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('vendor_login'), resp.url)
