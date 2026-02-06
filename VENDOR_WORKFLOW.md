# ShopSphere Vendor Workflow

## Complete Flow Implemented

### 1. **Vendor Registration**
- URL: `/vendor/register/`
- **Process**:
  - User fills registration form (username, email, password)
  - System creates User account
  - System creates Vendor record with status = **'pending'** (awaiting admin approval)
  - User shown message: "Registration successful! Your request has been sent to admin for approval"
  - Redirects to `/vendor/login/`

### 2. **Admin Approval (Backend Only)**
- Admin accesses Django admin panel: `/admin/`
- Admin finds vendor in `Vendor` model
- Admin changes status from `'pending'` to `'approved'`
- Only then can vendor login

### 3. **Vendor Login**
- URL: `/vendor/login/`
- **Process**:
  - User enters username and password
  - System checks if user has vendor_profile
  - System checks vendor status:
    - ✅ `'approved'` → Login allowed → Redirects to `/vendor/dashboard/`
    - ⏳ `'pending'` → Shows message "Your account is pending admin approval"
    - ❌ `'rejected'` → Shows message "Your account has been rejected"
    - 🚫 `'blocked'` → Shows message "Your account has been blocked"

### 4. **Vendor Dashboard & Pages** 
- **Protected Pages** (only for approved vendors):
  - `/vendor/dashboard/` - Dashboard
  - `/vendor/profile/` - Edit profile
  - `/vendor/products/` - View products
  - `/vendor/products/new/` - Add new product
  - `/vendor/products/<id>/edit/` - Edit product
  - `/vendor/products/<id>/delete/` - Delete product
  - `/vendor/orders/` - View orders

- **Access Check**: Each page checks if vendor.status == 'approved'
  - If NOT approved → Shows error message → Redirects to login

### 5. **Add Products**
- URL: `/vendor/products/new/`
- **Process**:
  - Vendor fills product form
  - Selects category from dropdown (12 categories available)
  - Products created with status = **'active'** (appears on homepage)
  - Can upload multiple product images
  - Redirects to `/vendor/products/` list

### 6. **View Products**
- URL: `/vendor/products/`
- Shows all products added by vendor
- Can edit or delete products

### 7. **Homepage Display**
- URL: `/`
- Shows featured active products from all approved vendors
- Only products with status='active' and is_featured=True are shown

### 8. **Logout**
- URL: `/vendor/logout/`
- **Process**:
  - User clicks logout button
  - Session destroyed
  - Shows success message: "You have been logged out successfully!"
  - Redirects to `/vendor/login/`

---

## Database Status Values
```
Vendor.status choices:
  - 'pending'   → Awaiting admin approval (default for new vendors)
  - 'approved'  → Can login and use vendor features
  - 'rejected'  → Cannot login (registration rejected)
  - 'blocked'   → Cannot login (account blocked by admin)

Product.status choices:
  - 'active'    → Visible on homepage (default)
  - 'inactive'  → Hidden from homepage
  - 'blocked'   → Blocked by admin
```

---

## User Experience Flow

```
1. User visits /vendor/register/
   ↓
2. User registers (username, email, password)
   ↓
3. System creates vendor account with status='pending'
   ↓
4. User sees: "Request sent to admin for approval"
   ↓
5. User redirected to /vendor/login/
   ↓
6. User tries to login
   ↓
7. System checks vendor status
   - If pending → "Account pending approval. Check later."
   - If approved → Login successful → Redirect to /vendor/dashboard/
   ↓
8. Vendor Dashboard opens
   ↓
9. Vendor adds products (with categories)
   ↓
10. Products appear on homepage (status='active')
   ↓
11. Vendor clicks Logout
   ↓
12. User logged out → Redirected to /vendor/login/
```

---

## Testing
All workflows tested with 6 comprehensive tests:
- ✅ `test_vendor_registration_creates_pending_vendor`
- ✅ `test_pending_vendor_cannot_login`
- ✅ `test_approved_vendor_can_login`
- ✅ `test_vendor_logout_redirects_to_vendor_login`
- ✅ `test_approved_vendor_can_create_product`
- ✅ `test_dashboard_restricted_to_approved_vendors`

All tests PASS ✓
