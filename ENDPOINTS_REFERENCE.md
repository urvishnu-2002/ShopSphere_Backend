# ShopSphere API Endpoints Reference

## Quick Reference by Feature

### 🛍️ Shopping (Customer)
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| Browse Products | GET | `/api/vendor/products/` | Optional | Browse all active products |
| Product Details | GET | `/api/vendor/products/{id}/` | Optional | Get single product |
| Add to Cart | POST | `/api/customer/cart/add_item/` | Required | Add product to cart |
| View Cart | GET | `/api/customer/cart/get_cart/` | Required | Get cart contents |
| Update Item | POST | `/api/customer/cart/update_item/` | Required | Change quantity |
| Remove Item | POST | `/api/customer/cart/remove_item/` | Required | Delete from cart |
| Clear Cart | POST | `/api/customer/cart/clear_cart/` | Required | Empty cart |
| Create Order | POST | `/api/customer/orders/create_order/` | Required | Checkout from cart |
| Order History | GET | `/api/customer/orders/my_orders/` | Required | View all orders |
| Order Details | GET | `/api/customer/orders/order_detail/` | Required | Single order details |
| Cancel Order | POST | `/api/customer/orders/cancel_order/` | Required | Cancel pending order |

### 📦 Products (Vendor/Public)
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| List Products | GET | `/api/vendor/products/` | Optional | Paginated product list |
| Create Product | POST | `/api/vendor/products/` | Required* | Add new product |
| Get Product | GET | `/api/vendor/products/{id}/` | Optional | Product details |
| Update Product | PUT/PATCH | `/api/vendor/products/{id}/` | Required* | Edit product |
| Delete Product | DELETE | `/api/vendor/products/{id}/` | Required* | Remove product |
| My Products | GET | `/api/vendor/products/my_products/` | Required* | Vendor's products |
| Featured Products | GET | `/api/vendor/products/featured/` | Optional | Get featured items |
| Add Image | POST | `/api/vendor/products/{id}/add_image/` | Required* | Upload product image |
| Product Reviews | GET | `/api/vendor/products/{id}/reviews/` | Optional | Get all reviews |

**Auth Required* = Vendor only

### 👥 Vendors
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| List Vendors | GET | `/api/vendor/vendors/` | Admin | All vendors |
| My Profile | GET | `/api/vendor/vendors/my_profile/` | Vendor | Vendor's profile |
| Update Profile | PUT/PATCH | `/api/vendor/vendors/{id}/` | Vendor | Edit vendor info |
| Commissions | GET | `/api/vendor/vendors/{id}/commissions/` | Vendor/Admin | View commissions |
| Sales Report | GET | `/api/vendor/vendors/{id}/sales_report/` | Admin | Revenue report |

### 💰 Commissions
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| List Commissions | GET | `/api/vendor/commissions/` | Vendor/Admin | All commissions |
| Filter Status | GET | `/api/vendor/commissions/?status=pending` | Vendor/Admin | By status |

### 📋 Categories
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| List Categories | GET | `/api/vendor/categories/` | Optional | All categories |
| Category Details | GET | `/api/vendor/categories/{id}/` | Optional | Single category |

### 👤 Customer Account
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| Register | POST | `/api/customer/auth/register/` | - | Create account |
| View Profile | GET | `/api/customer/profile/profile/` | Required | Customer details |
| Update Profile | PUT/PATCH | `/api/customer/profile/profile/` | Required | Edit profile |

### ⭐ Reviews
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| Add Review | POST | `/api/customer/reviews/add_review/` | Required | Leave product review |

### 🎁 Wishlist
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| View Wishlist | GET | `/api/customer/wishlist/get_wishlist/` | Required | All wishlisted items |
| Add to Wishlist | POST | `/api/customer/wishlist/add_item/` | Required | Save product |
| Remove Item | POST | `/api/customer/wishlist/remove_item/` | Required | Remove from wishlist |

### 🚚 Delivery (Agent)
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| Agent Profile | GET | `/api/agent/agents/my_profile/` | Agent | Agent details |
| Toggle Availability | POST | `/api/agent/agents/availability/` | Agent | Set online/offline |
| My Deliveries | GET | `/api/agent/deliveries/my_deliveries/` | Agent | Assigned deliveries |
| Delivery Details | GET | `/api/agent/deliveries/delivery_detail/` | Agent | Single delivery |
| Update Status | POST | `/api/agent/deliveries/update_status/` | Agent | Change status |
| Assign Delivery | POST | `/api/agent/deliveries/assign_delivery/` | Admin | Allocate delivery |
| All Deliveries | GET | `/api/agent/deliveries/all_deliveries/` | Admin | All deliveries |

### ✅ Vendor Approval (Admin)
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| Pending Approvals | GET | `/api/admin/approvals/pending_approvals/` | Admin | New applications |
| All Approvals | GET | `/api/admin/approvals/all_approvals/` | Admin | All vendors |
| Approve Vendor | POST | `/api/admin/approvals/approve_vendor/` | Admin | Accept vendor |
| Reject Vendor | POST | `/api/admin/approvals/reject_vendor/` | Admin | Decline vendor |

### 💳 Commission Admin
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| All Commissions | GET | `/api/admin/commissions/all_commissions/` | Admin | All commissions |
| Pending | GET | `/api/admin/commissions/pending_commissions/` | Admin | Waiting payment |
| Mark Paid | POST | `/api/admin/commissions/mark_paid/` | Admin | Complete payment |

### 📊 Admin Dashboard
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| Statistics | GET | `/api/admin/dashboard/stats/` | Admin | Platform metrics |
| Recent Orders | GET | `/api/admin/dashboard/recent_orders/` | Admin | Latest orders |
| Vendor Performance | GET | `/api/admin/dashboard/vendor_performance/` | Admin | Sales by vendor |

### ⚙️ Settings (Admin)
| Feature | Method | Endpoint | Auth | Description |
|---------|--------|----------|------|-------------|
| Current Settings | GET | `/api/admin/settings/current/` | Admin | Platform config |
| Update Settings | PUT | `/api/admin/settings/{id}/` | Admin | Edit settings |

## Query Parameters

### Filtering
```
?category=1              Filter by category
?vendor=5                Filter by vendor
?status=active           Filter by status
?is_featured=true        Only featured
?city=NewYork            Filter by city
?status=pending          Filter by approval status
```

### Searching
```
?search=shirt            Search name/description
?search=electronics      Full-text search
```

### Ordering/Sorting
```
?ordering=name           Sort A-Z
?ordering=-price         Sort by price desc
?ordering=created_at     Sort by date
?ordering=-rating        Sort by rating desc
```

### Pagination
```
?page=1                  First page
?page=2                  Second page (12 items default)
?page_size=20            20 items per page
```

## Common Request Headers

```
Authorization: Token YOUR_AUTH_TOKEN    # API authentication
Content-Type: application/json           # JSON data
Accept: application/json                 # Expected response format
```

## Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST (creation) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid data sent |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | Wrong HTTP method |
| 500 | Server Error | Backend error |

## Request/Response Formats

### List Response
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/vendor/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Product Name",
      ...
    }
  ]
}
```

### Error Response
```json
{
  "error": "You must be a vendor to create products"
}
```

or

```json
{
  "field_name": ["Error message"]
}
```

## Delivery Status Workflow

```
assigned
  ↓
picked_up
  ↓
in_transit
  ↓
out_for_delivery
  ↓
delivered ✓

Alternative paths:
failed → cancelled
```

## Order Status Workflow

```
pending → confirmed → processing → shipped → delivered ✓

Alternative paths:
pending → cancelled
delivered → returned
```

## Vendor Approval Workflow

```
pending → under_review → approved ✓
              ↓
           rejected
```

## Product Status

- `active` - Available for purchase
- `inactive` - Not visible to customers
- `blocked` - Removed by admin

## Commission Status

- `pending` - Awaiting payment to vendor
- `paid` - Commission paid
- `cancelled` - Cancelled commission

## Agent Status

- `active` - Available for deliveries
- `inactive` - Temporarily unavailable
- `suspended` - Permanently unavailable

## Common Task Examples

### Get Featured Products
```
GET /api/vendor/products/?is_featured=true&ordering=-created_at
```

### Get Pending Vendor Approvals
```
GET /api/admin/approvals/pending_approvals/
```

### Filter Orders by Status
```
GET /api/customer/orders/my_orders/?status=pending
```

### Search Products
```
GET /api/vendor/products/?search=shirt&ordering=-rating
```

### Get Agent's Pending Deliveries
```
GET /api/agent/deliveries/my_deliveries/?status=assigned
```

### Get All Pending Commissions
```
GET /api/admin/commissions/pending_commissions/
```

## Rate Limiting

Currently no rate limiting implemented. For production, consider adding via `django-ratelimit` or API gateway.

## Pagination Default

- **Default Page Size**: 12 items
- **Customizable**: `?page_size=20`
- **Format**: DRF PageNumberPagination

---

For detailed examples and request bodies, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
