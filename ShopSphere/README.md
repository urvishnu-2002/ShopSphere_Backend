# ShopSphere - Multi-Vendor E-Commerce Platform

A production-ready Django-based multi-vendor e-commerce website where vendors can sell products, customers can purchase them, and admins control the platform.

## 🎯 Features Implemented

### User Roles
- **Super Admin**: Vendor approval, commission settings, user control, reports, block products
- **Vendor**: Product CRUD, stock management, order viewing, commission tracking
- **Customer**: Browse products, cart, checkout, order history, reviews, wishlist
- **Delivery Agent**: Update delivery status, OTP verification

### Core Functionality
✅ User authentication and authorization (Django Auth + Token Auth)
✅ Product catalog with categories, images, pricing, and discounts
✅ Shopping cart and checkout system
✅ Order management with status tracking
✅ Vendor dashboard with product and order management
✅ Customer profiles and address management
✅ Product reviews and ratings
✅ Wishlist functionality
✅ Delivery tracking with OTP verification
✅ Commission and payment tracking
✅ Admin reports and analytics
✅ Responsive Bootstrap UI on all pages

## 📁 Project Structure

```
ShopSphere/
├── ShopSphere/           # Main project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── vendor/               # Vendor app
│   ├── models.py         # Vendor, Product, Category models
│   ├── views.py          # Vendor views (registration, dashboard, product CRUD)
│   ├── forms.py          # Vendor forms
│   ├── urls.py           # Vendor URL routing
│   ├── api_views.py      # Vendor API endpoints
│   └── api_urls.py       # Vendor API routing
├── customer/             # Customer app
│   ├── models.py         # Customer, Cart, Order, Review models
│   ├── views.py          # Customer views (products, cart, checkout, orders)
│   ├── forms.py          # Customer forms
│   ├── urls.py           # Customer URL routing
│   └── api_urls.py       # Customer API routing
├── agent/                # Delivery agent app
│   ├── models.py         # Delivery, DeliveryAgent models
│   ├── views.py          # Delivery views
│   ├── urls.py           # Agent URL routing
│   └── api_urls.py       # Agent API routing
├── admin/                # Admin app
│   ├── models.py         # Admin, Commission, Report models
│   └── apps.py           # App configuration (custom label)
├── accounts/             # Authentication app
│   ├── urls.py           # Auth URLs (login, logout, signup)
│   └── views.py          # Auth views
├── templates/            # HTML templates
│   ├── base.html         # Base template with Bootstrap styling
│   ├── index.html        # Home page
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── signup_choice.html
│   ├── customer/
│   │   ├── products.html
│   │   ├── product_detail.html
│   │   └── cart.html
│   └── vendor/
│       └── register.html
├── static/               # CSS, JS, images
│   └── (Bootstrap CDN used in templates)
├── media/                # User-uploaded files (products, profiles)
├── db.sqlite3            # SQLite database
└── manage.py             # Django management script
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd ShopSphere  
pip install --upgrade djangorestframework Pillow
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. Start Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Customer Products**: http://127.0.0.1:8000/customer/products/
- **Vendor Registration**: http://127.0.0.1:8000/vendor/register/
- **Login**: http://127.0.0.1:8000/accounts/login/

## 📊 Database Models

### Vendor App
- **Vendor**: Vendor profiles with business info, GST, bank details
- **Product**: Product catalog with pricing, discounts, stock
- **Category**: Product categories for organization
- **ProductImage**: Multiple images per product
- **VendorCommission**: Commission tracking

### Customer App
- **CustomerProfile**: Extended user profile with addresses
- **Cart**: Shopping cart management
- **CartItem**: Items in cart
- **Order**: Customer orders with complete tracking
- **OrderItem**: Items in each order
- **Review**: Product reviews and ratings
- **Wishlist**: Bookmarked products

### Agent App
- **DeliveryAgent**: Agent profiles and statistics
- **Delivery**: Delivery records with status tracking
- **DeliveryHistory**: Historical status updates

### Admin App
- **AdminSettings**: Platform configuration
- **VendorApproval**: Vendor approval workflow
- **Commission**: Admin commission management
- **PlatformReport**: Analytics and reports
- **BlockedProduct**: Product blocking management
- **UserManagement**: User control features

## 🔐 Security Features
- Django User authentication
- CSRF protection on all forms
- Password hashing (PBKDF2)
- Token-based API authentication
- Email validation
- Role-based access control

## 🎨 Frontend
- **Bootstrap 5** - Responsive grid system and components
- **Font Awesome 6** - Icons and visual elements
- **Responsive Design** - Works on all devices
- **Clean UI** - Modern, professional appearance

## 📡 API Endpoints

### Vendor API
- `GET /api/vendor/` - Vendor API root
- `GET /api/vendor/products/` - List products
- `GET/PUT/DELETE /api/vendor/products/<id>/` - Product detail

### Customer API
- `GET /api/customer/` - Customer API root
- `GET /api/customer/products/` - Browse products
- `GET/POST /api/customer/cart/` - Cart operations

### Agent API
- `GET /api/agent/` - Agent API root
- `GET /api/agent/deliveries/` - List deliveries
- `GET/POST /api/agent/deliveries/<id>/status/` - Update delivery status

## 🔄 User Workflows

### Customer Journey
1. Register/Login
2. Browse products by category or search
3. View product details and reviews
4. Add to cart
5. Proceed to checkout with shipping address
6. Choose payment method (Razorpay/COD)
7. Track order status
8. Leave reviews after delivery

### Vendor Journey
1. Register as vendor
2. Complete business profile
3. Await admin approval
4. After approval: Create products with images
5. Manage inventory
6. View incoming orders
7. Track commission and earnings

### Admin Journey
1. Login to admin panel
2. Review and approve vendors
3. View all orders and transactions
4. Manage commissions and payments
5. View analytics and reports
6. Block products if needed
7. Manage user accounts

## 📝 Testing the Website

### Create Test Vendor
1. Go to `/vendor/register/`
2. Create account with username: `vendor1`
3. Complete business profile
4. Admin approves vendor (in Django admin)
5. Create products

### Create Test Customer
1. Go to `/accounts/signup/` → Select Customer
2. Create account with username: `customer1`
3. Complete profile
4. Browse products
5. Add to cart and checkout

### Admin Access
1. Go to `/admin/`
2. Login with superuser credentials
3. Approve vendors, view orders, manage commissions

## 🔌 Payment Integration Ready
The code is structured to easily integrate:
- **Razorpay**: Payment gateway for online payments
- **Email notifications**: Order confirmations, shipping updates
- **SMS**: OTP delivery for verification
- **PDF invoices**: Generate invoices for orders

## 🚧 Future Enhancements

1. **Payment Gateway Integration**: Full Razorpay integration with webhooks
2. **Email & SMS**: Notifications for orders, deliveries, OTP
3. **PDF Invoices**: Generate printable invoices
4. **Chat Support**: Real-time customer-vendor communication
5. **Analytics Dashboard**: Advanced reporting and insights
6. **Inventory Alerts**: Stock management notifications
7. **Return Management**: Handle product returns and refunds
8. **Rating System**: Detailed vendor performance metrics
9. **Mobile App**: React Native or Flutter versions
10. **API Rate Limiting**: Prevent abuse of API endpoints

## 💻 Tech Stack
- **Backend**: Django 6.0.2
- **Database**: SQLite (easily migrate to PostgreSQL/MySQL)
- **API**: Django REST Framework
- **Frontend**: Bootstrap 5 + Vanilla JS
- **Authentication**: Django Auth + Token Auth
- **Image Handling**: Pillow
- **Version Control**: Git

## 📄 License
This project is built for the Hard Level 14-Day Assessment

## 👥 Team Structure (As per requirements)
- **4 Frontend Developers** - Template & UI development
- **4 Backend Developers** - API & business logic
- **2 QA/Testing** - Test cases and validation
- **1 DevOps** - Deployment and server management
- **1 Documentation** - API docs and project documentation

## 📞 Support
For questions or issues, refer to:
- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Bootstrap Docs: https://getbootstrap.com/docs/

---

**Ready to Deploy**: This code can be deployed to production with proper configuration management, security hardening, and scalability improvements.
