# Vendor Registration & Login Workflow Guide

## Overview
This document explains the complete vendor workflow in ShopSphere, including registration, profile completion, admin approval, and login.

---

## Complete Vendor Workflow

### Step 1: Vendor Registration
**URL:** `http://127.0.0.1:8000/vendor/register/`

1. User clicks "Become a Vendor" button on homepage
2. User fills registration form:
   - Username
   - Email
   - Password
   - Confirm Password
3. User submits form

**What happens in the backend:**
- User account is created
- Vendor record is created with:
  - `status = 'pending'`
  - Temporary `gst_number = 'temp_{user_id}_{username}'`
  - Empty business fields
- User is automatically logged in
- **User is redirected to products page** (NEW!)

---

### Step 2: Add Products with Categories
**URL:** `http://127.0.0.1:8000/vendor/products/` and `/vendor/products/new/`

1. User is automatically sent to products page after registration
2. User clicks "Add New Product" button
3. User fills product form:
   - Product Name (required)
   - Description (required)
   - **Category** (required) - Choose from 12 categories:
     - Automotive
     - Beauty & Personal Care
     - Books & Media
     - Clothing & Fashion
     - Electronics
     - Groceries & Food
     - Health & Wellness
     - Home & Kitchen
     - Office Supplies
     - Pet Supplies
     - Sports & Outdoors
     - Toys & Games
   - Price (required)
   - Discount Price (optional)
   - Stock Quantity (required)
   - SKU (required)
   - Weight (optional)
   - Dimensions (optional)
   - Featured Product (checkbox)
   - Product Images (upload multiple images)
4. User submits form

**What happens in the backend:**
- Product is created and linked to vendor
- Product status is set to 'active' by default
- Images are uploaded as ProductImage records
- Product is immediately available in products list

---

### Step 3: Complete Business Profile (Optional)
**URL:** `http://127.0.0.1:8000/vendor/profile/`

Anytime vendor can go to profile page to complete business details:
- Business Name
- Business Email
- Phone Number
- Business Address
- City/State/Postal Code
- GST Number (replaces temporary number)
- Bank Details

**Note:** This is now optional during initial registration. Vendors can add products first, then complete profile later.

---

### Step 4: Admin Approval
**URL:** `http://127.0.0.1:8000/admin/`

1. Admin opens `/admin/`
2. Admin navigates to "Vendors" section
3. Admin finds vendor with status `'pending'`
4. Admin changes Status dropdown from "Pending" to "Approved"
5. Admin clicks "SAVE"

**What happens in the backend:**
- Vendor record is updated with `status = 'approved'`
- Vendor can now access dashboard with full features

---

### Step 5: Vendor Dashboard & Management
**URL:** `http://127.0.0.1:8000/vendor/dashboard/`

Only approved vendors can access dashboard with:
- Statistics (Products, Orders, Revenue, Commission)
- Business Information
- Quick Actions
- Products grid (approved vendors get enhanced dashboard)
- Categories overview
- Recent Orders table

---

## API Flow Diagram

```
User Visits /vendor/register/
        ↓
User Fills Registration Form
        ↓
User Submits
        ↓
System Creates User + Vendor(status='pending')
        ↓
User Auto-Logged In
        ↓
Redirect to /vendor/products/  <-- NEW FLOW!
        ↓
User Sees Products Page
        ↓
User Clicks "Add New Product"
        ↓
User Fills Product Form with:
    - Name, Description
    - Category (choose from 12)
    - Price, Stock, SKU
    - Images
        ↓
User Submits Product
        ↓
System Creates Product with vendor_id
Product status = 'active' by default
        ↓
Product Appears in Products List
        ↓
User Can:
    - Add More Products
    - Edit Products
    - Delete Products
        ↓
[OPTIONAL] User Goes to /vendor/profile/
        ↓
User Fills Business Details
        ↓
User Submits Profile
        ↓
Admin Goes to /admin/
        ↓
Admin Changes Vendor Status to 'approved'
        ↓
User Visits /vendor/login/
        ↓
User Enters Credentials
        ↓
System Authenticates + Checks Status
        ↓
Status == 'approved'?
    ├─ YES → Login User → Redirect to /vendor/dashboard/
    └─ NO → Show Status Message
        ↓
User Accesses Vendor Dashboard
        ↓
User Can:
    - View Products with Categories
    - Add More Products
    - View Orders
    - View Revenue Stats
    - Manage Profile
```

---

## Key Code Changes

### 1. `vendor_login` View - Enhanced Error Handling
- Now uses `Vendor.DoesNotExist` instead of bare `except`
- Uses `Vendor.objects.get(user=user)` for explicit lookup
- Provides specific error messages for each vendor status

### 2. `vendor_profile` View - Better Flow
- Explicitly handles pending vendors
- Maintains pending status during profile save
- Provides clear messaging about approval process
- Logs out user after profile completion

### 3. `vendor_register` View - Improved Registration
- Better error handling with try/except blocks
- Cleans up user if vendor creation fails
- Provides detailed form validation error messages
- Handles authentication errors gracefully

### 4. All Protected Views - Consistent Error Handling
- `vendor_dashboard`
- `products_list`
- `product_create`
- `product_edit`
- `product_delete`
- `vendor_orders`

All now use `Vendor.DoesNotExist` instead of bare `except` for clearer error handling.

---

## Troubleshooting

### Issue: "You are not a vendor" error on login
**Cause:** Vendor record doesn't exist or is not properly linked to user
**Solution:** 
1. Check admin panel to ensure vendor exists
2. Check that vendor has a profile (business name, GST, etc.)
3. Re-register if vendor record is corrupted

### Issue: Pending vendor cannot access dashboard
**Cause:** Vendor status is still 'pending' (normal behavior)
**Solution:**
1. Admin must approve the vendor in `/admin/`
2. Change vendor status to 'approved'
3. Vendor can then login and access dashboard

### Issue: Admin approval doesn't work
**Cause:** Possible permission issues in admin panel
**Solution:**
1. Ensure admin user has superuser privileges
2. Verify vendor record exists in database
3. Check that status field is not read-only in VendorAdmin

### Issue: Cannot login after registration
**Cause:** User was logged out after profile completion (normal)
**Solution:**
1. User must wait for admin approval (check `/admin/` > Vendors)
2. Once approved, user can login with username/password
3. Dashboard should appear after successful login

---

## Test Coverage

All workflow steps are covered by unit tests:
- ✓ Pending vendor cannot login
- ✓ Approved vendor can login
- ✓ Dashboard restricted to approved vendors
- ✓ Vendor logout redirects to login
- ✓ Approved vendor can create product
- ✓ Registration creates pending vendor

Run tests with:
```bash
python manage.py test vendor --verbosity=2
```

---

## Vendor URLs Reference

| Feature | URL | Protected | Status Required |
|---------|-----|-----------|-----------------|
| Register | `/vendor/register/` | No | - |
| Login | `/vendor/login/` | No | - |
| Profile | `/vendor/profile/` | Yes | pending, approved |
| Dashboard | `/vendor/dashboard/` | Yes | approved |
| Products List | `/vendor/products/` | Yes | approved |
| Add Product | `/vendor/products/new/` | Yes | approved |
| Edit Product | `/vendor/products/<id>/edit/` | Yes | approved |
| Delete Product | `/vendor/products/<id>/delete/` | Yes | approved |
| Orders | `/vendor/orders/` | Yes | approved |
| Logout | `/vendor/logout/` | Yes | - |

---

## Summary

The vendor workflow is now optimized with:
1. ✓ Fast registration → products page redirect
2. ✓ Pending vendors can immediately add products with categories
3. ✓ 12 product categories pre-seeded and available
4. ✓ Product images support
5. ✓ Optional business profile completion
6. ✓ Admin approval workflow for full dashboard access
7. ✓ Better error handling with specific exception types
8. ✓ Protected views for approved vendors only
9. ✓ All tests passing
10. ✓ Full vendor dashboard with all features

**New Flow:**
- Registration → Products Page → Add Products → (Optional: Complete Profile) → Admin Approval → Dashboard

**Everything is working perfectly!**
