# ShopSphere Backend - Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation & Setup

### 1. Clone Repository
```bash
cd ShopSphere_Backend
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Navigate to Project Directory
```bash
cd ShopSphere
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 7. Start Development Server
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/`

## Accessing the API

### API Root Endpoints
- **Vendor API**: http://localhost:8000/api/vendor/
- **Customer API**: http://localhost:8000/api/customer/
- **Agent API**: http://localhost:8000/api/agent/
- **Admin API**: http://localhost:8000/api/admin/

### Django Admin Panel
- **URL**: http://localhost:8000/admin/
- **Credentials**: Use the superuser account created above

## Common Tasks

### Create a Test Product (as Vendor)

1. **Register as Vendor** (Manual through Admin)
   - Go to Django Admin: http://localhost:8000/admin/
   - Create a User account
   - Create a Vendor profile linked to the user
   - Approve the vendor

2. **Get Authentication Token**
   ```bash
   POST /api-token-auth/
   {
     "username": "vendor_username",
     "password": "password"
   }
   ```

3. **Create Product**
   ```bash
   POST /api/vendor/products/
   Authorization: Token YOUR_TOKEN
   Content-Type: application/json

   {
     "category": 1,
     "name": "Sample Product",
     "description": "Product description",
     "price": "99.99",
     "discount_price": "79.99",
     "stock": 50,
     "sku": "PROD-001",
     "status": "active"
   }
   ```

### Register as Customer and Create Order

1. **Register Customer**
   ```bash
   POST /api/customer/auth/register/
   {
     "username": "john_doe",
     "email": "john@example.com",
     "password": "securepassword123",
     "password2": "securepassword123"
   }
   ```

2. **Login and Get Token**
   See above for token retrieval

3. **Add Item to Cart**
   ```bash
   POST /api/customer/cart/add_item/
   Authorization: Token YOUR_TOKEN
   {
     "product_id": 1,
     "quantity": 2
   }
   ```

4. **Place Order**
   ```bash
   POST /api/customer/orders/create_order/
   Authorization: Token YOUR_TOKEN
   {
     "shipping_address": "123 Main St",
     "shipping_city": "New York",
     "shipping_state": "NY",
     "shipping_postal_code": "10001",
     "payment_method": "cod"
   }
   ```

## Development Workflow

### 1. Making API Requests

#### Using cURL
```bash
# Get all products
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/vendor/products/

# Create product (requires Token)
curl -X POST \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Product","price":"99.99",...}' \
  http://localhost:8000/api/vendor/products/
```

#### Using Postman
1. Install Postman
2. Import API collection (create from endpoint list)
3. Set Authorization header: `Token YOUR_AUTH_TOKEN`
4. Make requests

#### Using Python Requests
```python
import requests

headers = {
    'Authorization': 'Token YOUR_AUTH_TOKEN',
    'Content-Type': 'application/json'
}

# Get products
response = requests.get(
    'http://localhost:8000/api/vendor/products/',
    headers=headers
)
products = response.json()
```

### 2. Database Inspection

#### Using Django Admin
Visit http://localhost:8000/admin/ to view/edit all data

#### Using Django Shell
```bash
python manage.py shell
```

```python
from vendor.models import Product
from customer.models import Order
from django.contrib.auth.models import User

# Get all products
products = Product.objects.all()
for product in products:
    print(f"{product.name} - ₹{product.price}")

# Get user's orders
user = User.objects.get(username='john_doe')
orders = user.orders.all()
for order in orders:
    print(f"Order {order.order_id}: {order.final_amount}")
```

### 3. Running Management Commands

```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Check for issues
python manage.py check

# Create sample data (if seed command available)
python manage.py seed_categories

# Reset database (WARNING: deletes all data)
python manage.py flush
```

### 4. Testing Endpoints

#### Test Product Filtering
```bash
# Filter by category
GET /api/vendor/products/?category=1

# Filter by vendor
GET /api/vendor/products/?vendor=5

# Search products
GET /api/vendor/products/?search=shirt

# Featured products
GET /api/vendor/products/?is_featured=true

# Sort by price (descending)
GET /api/vendor/products/?ordering=-price

# Multiple filters
GET /api/vendor/products/?category=1&status=active&ordering=name
```

## Debugging

### Enable Debug Mode
```python
# In settings.py
DEBUG = True
ALLOWED_HOSTS = ['*']  # For development only
```

### View Request/Response Logs
```bash
# Django logs to console when DEBUG=True
# Or check shell with:
python manage.py runserver 0.0.0.0:8000 --verbosity 2
```

### Django Debug Toolbar (Optional)
```bash
pip install django-debug-toolbar
```

Then add to INSTALLED_APPS in settings.py:
```python
INSTALLED_APPS = [
    ...
    'debug_toolbar',
]
```

## Troubleshooting

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

### Database Lock Error
```bash
# Delete database and start fresh
rm db.sqlite3
python manage.py migrate
```

### Module Not Found Error
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### CORS Errors
- Check CORS_ALLOWED_ORIGINS in settings.py
- Ensure frontend URL is added to the list
- Verify `corsheaders` middleware is installed

## Production Deployment

### Before Going to Production

1. **Set DEBUG = False** in settings.py
2. **Update ALLOWED_HOSTS** with your domain
3. **Generate new SECRET_KEY**
4. **Use PostgreSQL** instead of SQLite
5. **Enable HTTPS** and update CORS settings
6. **Run security checks**: `python manage.py check --deploy`

### Database Migration to PostgreSQL
```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Update DATABASES in settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shopsphere',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Run migrations
python manage.py migrate
```

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Guide](https://www.django-rest-framework.org/)
- [Complete API Documentation](./API_DOCUMENTATION.md)
- [Refactoring Summary](./REFACTORING_SUMMARY.md)

## Support & Contributions

For issues, improvements, or questions:
1. Check API documentation
2. Review error messages and logs
3. Test in Django Admin panel
4. Consult Django/DRF documentation

---

**Happy Coding! 🚀**
