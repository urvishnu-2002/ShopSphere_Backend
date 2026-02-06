# Quick Start Guide - Vendor Flow

## New Vendor Registration Flow (Simplified!)

### Registration → Products Page → Add Products

---

## Step-by-Step Guide

### 1. Register
Go to: `http://127.0.0.1:8000/vendor/register/`

```
Fill in:
- Username
- Email
- Password
- Confirm Password

Click "Register"
```

**Result:** Automatically redirected to Products Page!

---

### 2. Add Products
Go to: `http://127.0.0.1:8000/vendor/products/new/`

```
Fill in Product Details:
- Product Name (required)
- Description (required)
- Category (required) ← Choose from 12 categories
- Price (required)
- Discount Price (optional)
- Stock Quantity (required)
- SKU (required)
- Weight (optional)
- Dimensions (optional)
- Is Featured (checkbox)
- Product Images (upload up to multiple images)

Click "Create Product"
```

**Result:** Product added with selected category!

---

### 3. Available Categories

| # | Category Name | Icon |
|---|---|---|
| 1 | Automotive | `fas fa-car` |
| 2 | Beauty & Personal Care | `fas fa-spa` |
| 3 | Books & Media | `fas fa-book` |
| 4 | Clothing & Fashion | `fas fa-shirt` |
| 5 | Electronics | `fas fa-laptop` |
| 6 | Groceries & Food | `fas fa-shopping-basket` |
| 7 | Health & Wellness | `fas fa-heartbeat` |
| 8 | Home & Kitchen | `fas fa-home` |
| 9 | Office Supplies | `fas fa-pen` |
| 10 | Pet Supplies | `fas fa-paw` |
| 11 | Sports & Outdoors | `fas fa-dumbbell` |
| 12 | Toys & Games | `fas fa-gamepad` |

---

### 4. (Optional) Complete Business Profile
Go to: `http://127.0.0.1:8000/vendor/profile/`

```
Fill in Business Details:
- Business Name
- Business Email
- Phone Number
- Business Address
- City
- State
- Postal Code
- GST Number
- Bank Account Number
- Bank IFSC Code
- Bank Name

Click "Save Profile"
```

**Note:** This is OPTIONAL during initial registration. You can do this anytime!

---

### 5. Wait for Admin Approval

Admin will review your account and approve it.

Once approved, you can:
- Login at `/vendor/login/`
- Access full vendor dashboard
- View orders and revenue stats

---

## Test Account

```
Username: testvendor
Password: testpass123
```

This vendor is already approved and can login directly to dashboard.

---

## URL Reference

| Feature | URL | Access After |
|---------|-----|---|
| Register | `/vendor/register/` | Immediately |
| Products List | `/vendor/products/` | After Registration |
| Add Product | `/vendor/products/new/` | After Registration |
| Edit Product | `/vendor/products/<id>/edit/` | After Registration |
| Delete Product | `/vendor/products/<id>/delete/` | After Registration |
| Profile | `/vendor/profile/` | After Registration |
| Login | `/vendor/login/` | After Registration |
| Dashboard | `/vendor/dashboard/` | After Admin Approval |
| Orders | `/vendor/orders/` | After Admin Approval |
| Logout | `/vendor/logout/` | After Login |

---

## What Changed?

### Old Flow:
```
Register → Profile Completion Form → Logout → Wait for Approval → Login → Dashboard
```

### New Flow (Much Better!):
```
Register → Products Page → Add Products with Categories → (Optional: Complete Profile) → Wait for Approval → Dashboard
```

---

## Features Available at Each Stage

### After Registration (Pending Vendor):
✓ Add Products  
✓ Manage Products (List, Edit, Delete)  
✓ Upload Product Images  
✓ Select Categories for Products  
✓ Complete Business Profile (Anytime)  

### After Admin Approval (Approved Vendor):
✓ Everything above, PLUS:  
✓ Access Vendor Dashboard  
✓ View Statistics (Products, Orders, Revenue)  
✓ View Business Information  
✓ View Orders  
✓ View Products with Categories  
✓ Access Full Dashboard Features  

---

## Key Points

1. **Fast Registration:** No lengthy profile form required upfront
2. **Immediate Productivity:** Start adding products right after registration
3. **12 Categories:** All products pre-categorized
4. **Image Support:** Upload multiple product images
5. **Flexible:** Complete business profile anytime
6. **Admin Review:** Account approved before full feature access

---

## Support

If you encounter any issues:
1. Check admin panel: `http://127.0.0.1:8000/admin/`
2. Verify vendor status
3. Ensure categories are available
4. Check product form for validation errors

---

**Ready to sell? Start registering vendors now!**
