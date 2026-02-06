# ShopSphere Backend API Documentation

## Overview
ShopSphere is a multi-vendor e-commerce platform backend built with Django REST Framework (DRF). All data is persisted in a Django SQLite3 database with proper models, serializers, and REST API endpoints.

## Architecture

### Technology Stack
- **Framework**: Django 6.0.2
- **API**: Django REST Framework 3.16.1
- **Database**: SQLite3 (configurable to PostgreSQL/MySQL)
- **Authentication**: Token-based + Session-based
- **Filtering**: django-filter + DRF SearchFilter
- **CORS**: django-cors-headers enabled

### Project Structure
```
ShopSphere_Backend/
├── ShopSphere/              # Main project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py
├── vendor/                # Vendor management
│   ├── models.py
│   ├── serializers.py    # DRF Serializers
│   ├── api_views.py      # API ViewSets
│   └── api_urls.py       # API Routes
├── customer/             # Customer management
│   ├── models.py
│   ├── serializers.py
│   ├── api_views.py
│   └── api_urls.py
├── agent/               # Delivery agents
│   ├── models.py
│   ├── serializers.py
│   ├── api_views.py
│   └── api_urls.py
├── admin/              # Platform administration
│   ├── models.py
│   ├── serializers.py
│   ├── api_views.py
│   └── api_urls.py
└── manage.py
```

## Database Models

### Vendor Models
- **Vendor**: Vendor profile with business details, commission rates, and approval status
- **Category**: Product categories
- **Product**: Product details with pricing, stock, and ratings
- **ProductImage**: Product images
- **ProductStock**: Stock management
- **VendorCommission**: Commission tracking

### Customer Models
- **CustomerProfile**: Extended customer profile
- **Cart**: Shopping cart
- **CartItem**: Items in cart
- **Order**: Customer orders with status tracking
- **OrderItem**: Items in order
- **Review**: Product reviews
- **Wishlist**: Product wishlist

### Agent Models
- **DeliveryAgent**: Delivery agent profiles
- **Delivery**: Delivery tracking and status

### Admin Models
- **AdminSettings**: Platform-wide settings
- **VendorApproval**: Vendor approval workflow
- **Commission**: Commission management

## API Endpoints

### Authentication
```
POST /api/customer/auth/register/     # Customer registration
GET  /api/customer/profile/profile/   # Get customer profile
PUT  /api/customer/profile/profile/   # Update customer profile
```

### Products (Vendor API)
```
GET    /api/vendor/categories/        # List all categories
POST   /api/vendor/products/          # Create product (vendor only)
GET    /api/vendor/products/          # List products
GET    /api/vendor/products/{id}/     # Get product details
PUT    /api/vendor/products/{id}/     # Update product (vendor only)
DELETE /api/vendor/products/{id}/     # Delete product (vendor only)
POST   /api/vendor/products/{id}/add_image/  # Add product image
GET    /api/vendor/products/featured/offline  # Get featured products
GET    /api/vendor/products/my_products/     # Get vendor's products
GET    /api/vendor/products/{id}/reviews/    # Get product reviews
```

### Vendor Management
```
GET    /api/vendor/vendors/          # List all vendors (admin)
GET    /api/vendor/vendors/my_profile/  # Get own vendor profile
PUT    /api/vendor/vendors/{id}/     # Update vendor profile
GET    /api/vendor/vendors/{id}/commissions/  # Get vendor commissions
GET    /api/vendor/vendors/{id}/sales_report/  # Sales report (admin)
GET    /api/vendor/commissions/      # Get commissions
```

### Commissions
```
GET   /api/vendor/commissions/       # List vendor commissions
GET   /api/vendor/commissions/?status=pending  # Filter by status
```

### Shopping Cart (Customer API)
```
GET  /api/customer/cart/get_cart/     # Get user's cart
POST /api/customer/cart/add_item/     # Add item to cart
POST /api/customer/cart/update_item/  # Update item quantity
POST /api/customer/cart/remove_item/  # Remove item from cart
POST /api/customer/cart/clear_cart/   # Clear cart
```

### Orders (Customer API)
```
POST /api/customer/orders/create_order/  # Create order from cart
GET  /api/customer/orders/my_orders/    # Get order history
GET  /api/customer/orders/order_detail/?order_id=ORD-XXX  # Get order details
POST /api/customer/orders/cancel_order/  # Cancel pending order
```

### Reviews (Customer API)
```
POST /api/customer/reviews/add_review/  # Add product review
```

### Wishlist (Customer API)
```
GET  /api/customer/wishlist/get_wishlist/  # Get customer's wishlist
POST /api/customer/wishlist/add_item/      # Add to wishlist
POST /api/customer/wishlist/remove_item/   # Remove from wishlist
```

### Delivery (Agent API)
```
GET  /api/agent/agents/my_profile/        # Get agent's profile
POST /api/agent/agents/availability/      # Toggle availability
GET  /api/agent/deliveries/my_deliveries/ # Get assigned deliveries
GET  /api/agent/deliveries/delivery_detail/?delivery_id=id  # Get delivery details
POST /api/agent/deliveries/update_status/ # Update delivery status
```

### Delivery Management (Admin)
```
GET  /api/agent/deliveries/all_deliveries/    # List all deliveries
POST /api/agent/deliveries/assign_delivery/   # Assign delivery to agent
```

### Vendor Approval (Admin API)
```
GET  /api/admin/approvals/pending_approvals/  # Get pending approvals
GET  /api/admin/approvals/all_approvals/      # Get all approvals
POST /api/admin/approvals/approve_vendor/     # Approve vendor
POST /api/admin/approvals/reject_vendor/      # Reject vendor
```

### Commission Management (Admin API)
```
GET  /api/admin/commissions/all_commissions/  # Get all commissions
GET  /api/admin/commissions/pending_commissions/  # Get pending commissions
POST /api/admin/commissions/mark_paid/        # Mark commission as paid
```

### Admin Dashboard
```
GET  /api/admin/dashboard/stats/             # Platform statistics
GET  /api/admin/dashboard/recent_orders/     # Recent orders
GET  /api/admin/dashboard/vendor_performance/  # Vendor metrics
```

### Platform Settings (Admin)
```
GET  /api/admin/settings/current/   # Get current platform settings
PUT  /api/admin/settings/{id}/      # Update settings (admin only)
```

## Request/Response Examples

### Register Customer
```bash
POST /api/customer/auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password2": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}

Response (201):
{
  "message": "User registered successfully",
  "username": "john_doe"
}
```

### Create Order
```bash
POST /api/customer/orders/create_order/
Authorization: Token YOUR_AUTH_TOKEN
Content-Type: application/json

{
  "shipping_address": "123 Main St",
  "shipping_city": "New York",
  "shipping_state": "NY",
  "shipping_postal_code": "10001",
  "payment_method": "cod"
}

Response (201):
{
  "message": "Order created successfully",
  "order": {
    "id": 1,
    "order_id": "ORD-ABC12345",
    "customer_email": "john@example.com",
    "total_amount": "1500.00",
    "final_amount": "1550.00",
    "order_status": "pending",
    "payment_status": "pending",
    "items": [...]
  }
}
```

### Add to Cart
```bash
POST /api/customer/cart/add_item/
Authorization: Token YOUR_AUTH_TOKEN
Content-Type: application/json

{
  "product_id": 42,
  "quantity": 2
}

Response (201):
{
  "message": "Item added to cart",
  "item": {
    "id": 1,
    "product": {...},
    "quantity": 2,
    "total_price": "500.00"
  }
}
```

### Create Product (Vendor)
```bash
POST /api/vendor/products/
Authorization: Token VENDOR_TOKEN
Content-Type: application/json

{
  "category": 1,
  "name": "Premium T-Shirt",
  "description": "High-quality cotton t-shirt",
  "price": "19.99",
  "discount_price": "14.99",
  "stock": 100,
  "sku": "TSH-001",
  "status": "active"
}

Response (201):
{
  "id": 42,
  "name": "Premium T-Shirt",
  ...
}
```

## Authentication

### Token Authentication
1. Register user via `/api/customer/auth/register/`
2. Django automatically creates Token on user creation
3. Include header: `Authorization: Token YOUR_AUTH_TOKEN`

### Permissions
- **AllowAny**: Public products list, category list
- **IsAuthenticated**: Cart, orders, reviews (customer only)
- **IsAdminUser**: Admin endpoints, vendor approvals
- **Custom Vendor Check**: Vendors can only manage their own products

## Data Validation

### Product Validation
- SKU must be unique
- Price must be > 0.01
- Discount price must be less than regular price
- Stock cannot be negative

### Vendor Validation
- GST number must be unique
- Business email must be valid
- Must be approved before selling

### Order Validation
- Cannot create order with empty cart
- Product stock must be sufficient
- Payment method is required

## Filtering & Search

### Example Filters
```bash
GET /api/vendor/products/?category=1                 # Filter by category
GET /api/vendor/products/?vendor=5                   # Filter by vendor
GET /api/vendor/products/?status=active              # Filter by status
GET /api/vendor/products/?is_featured=true           # Get featured products
GET /api/vendor/products/?search=shirt               # Search by name/description
GET /api/vendor/products/?ordering=-price            # Sort by price (descending)
GET /api/vendor/products/?page=2                     # Pagination (12 items/page)
```

## Pagination
Default page size: 12 items
```bash
GET /api/vendor/products/?page=2&page_size=20
```

## Error Handling

### Common Error Responses
```json
{
  "detail": "Not authenticated.",
  "status_code": 401
}
```

```json
{
  "error": "You must be a vendor to create products",
  "status_code": 403
}
```

```json
{
  "sku": ["This SKU already exists."],
  "status_code": 400
}
```

## CORS Configuration
Configured for:
- localhost:3000 (frontend development)
- localhost:8000 (backend)
- 127.0.0.1:3000
- 127.0.0.1:8000

## Database Persistence
All data is stored in Django SQLite3 database:
- Products and inventory
- Customer orders and payments
- Vendor commissions
- Reviews and ratings
- Delivery tracking
- User accounts and authentication tokens

## Setup Instructions

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run Migrations**
```bash
python manage.py migrate
```

3. **Create Superuser**
```bash
python manage.py createsuperuser
```

4. **Run Development Server**
```bash
python manage.py runserver
```

5. **Access Admin Panel**
Navigate to `http://localhost:8000/admin/`

## Future Enhancements
- Payment gateway integration (Razorpay)
- Email notifications
- SMS notifications
- Advanced analytics
- Inventory management system
- Return/Refund management
- Multi-language support
