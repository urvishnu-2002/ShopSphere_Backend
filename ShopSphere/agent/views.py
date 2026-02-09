from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AgentRegistrationForm
from .models import Agent

# ===== Dummy Agents =====
DUMMY_AGENTS = [
    {'id': 1, 'username': 'agent_john', 'email': 'john@example.com'},
    {'id': 2, 'username': 'agent_sara', 'email': 'sara@example.com'},
    {'id': 3, 'username': 'agent_mike', 'email': 'mike@example.com'},
    {'id': 4, 'username': 'agent_lisa', 'email': 'lisa@example.com'},
    {'id': 5, 'username': 'agent_tom', 'email': 'tom@example.com'},
]

# ===== Dummy Orders =====
DUMMY_ORDERS = [
    {'id': 1, 'order_id': 'ORD-001', 'customer_name': 'John Doe', 'delivery_address': '123 Main Street, New York, NY 10001', 'earning': 10.00, 'status': 'AVAILABLE'},
    {'id': 2, 'order_id': 'ORD-002', 'customer_name': 'Jane Smith', 'delivery_address': '456 Oak Avenue, Brooklyn, NY 11201', 'earning': 12.50, 'status': 'AVAILABLE'},
    {'id': 3, 'order_id': 'ORD-003', 'customer_name': 'Michael Johnson', 'delivery_address': '789 Pine Road, Queens, NY 11375', 'earning': 8.00, 'status': 'AVAILABLE'},
    {'id': 4, 'order_id': 'ORD-004', 'customer_name': 'Alice Brown', 'delivery_address': '321 Elm Street, Bronx, NY 10453', 'earning': 15.00, 'status': 'DELIVERED'},
    {'id': 5, 'order_id': 'ORD-005', 'customer_name': 'Charlie Davis', 'delivery_address': '654 Maple Avenue, Brooklyn, NY 11215', 'earning': 9.50, 'status': 'DELIVERED'},
    {'id': 6, 'order_id': 'ORD-006', 'customer_name': 'Diana Evans', 'delivery_address': '888 Cedar Court, Staten Island, NY 10301', 'earning': 11.00, 'status': 'AVAILABLE'},
    {'id': 7, 'order_id': 'ORD-007', 'customer_name': 'Brian Lee', 'delivery_address': '111 Willow Lane, Manhattan, NY 10022', 'earning': 14.00, 'status': 'AVAILABLE'},
    {'id': 8, 'order_id': 'ORD-008', 'customer_name': 'Sara Wilson', 'delivery_address': '222 Birch Street, Queens, NY 11373', 'earning': 7.50, 'status': 'AVAILABLE'},
    {'id': 9, 'order_id': 'ORD-009', 'customer_name': 'Tom Harris', 'delivery_address': '333 Aspen Ave, Bronx, NY 10456', 'earning': 13.00, 'status': 'AVAILABLE'},
    {'id': 10, 'order_id': 'ORD-010', 'customer_name': 'Olivia Martin', 'delivery_address': '444 Oak Lane, Manhattan, NY 10011', 'earning': 16.00, 'status': 'AVAILABLE'},
]

# ===== Agent Portal View =====
def agent_portal(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('delivery_dashboard')

    login_form = AuthenticationForm()
    signup_form = AgentRegistrationForm()
    active_tab = 'signin'

    style = (
        'w-full p-5 bg-gray-50 border-2 border-gray-100 rounded-[2rem] '
        'font-bold tracking-wide focus:border-[#5D56D1] outline-none transition-all'
    )
    for field in login_form.fields.values():
        field.widget.attrs.update({'class': style})

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'signup':
            active_tab = 'signup'
            signup_form = AgentRegistrationForm(request.POST)

            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, "Account created! Welcome to the fleet 🚚")
                return redirect('delivery_dashboard')
            else:
                messages.error(request, "Please fix the errors below.")

        elif action == 'login':
            active_tab = 'signin'
            login_form = AuthenticationForm(request, data=request.POST)
            for field in login_form.fields.values():
                field.widget.attrs.update({'class': style})

            if login_form.is_valid():
                login(request, login_form.get_user())
                return redirect('delivery_dashboard')
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'agent_portal.html', {
        'login_form': login_form,
        'signup_form': signup_form,
        'active_tab': active_tab,
        'dummy_agents': DUMMY_AGENTS,
    })


# ===== Delivery Dashboard View =====
@login_required
def delivery_dashboard(request):
    if not isinstance(request.user, Agent):
        return redirect('agent_portal')

    # Active orders for dashboard
    active_order = next((o for o in DUMMY_ORDERS if o['status'] == 'AVAILABLE'), None)

    # Recent delivered orders
    recent_orders = [o for o in DUMMY_ORDERS if o['status'] == 'DELIVERED']

    # Dashboard stats
    total_earnings = sum(o['earning'] for o in recent_orders)
    completed_orders_count = len(recent_orders)
    available_orders_count = len([o for o in DUMMY_ORDERS if o['status'] == 'AVAILABLE'])

    return render(request, 'delivery_dashboard.html', {
        'user': request.user,
        'available_orders': [o for o in DUMMY_ORDERS if o['status'] == 'AVAILABLE'],
        'recent_orders': recent_orders,
        'total_earnings': total_earnings,
        'completed_orders_count': completed_orders_count,
        'available_orders_count': available_orders_count,
    })


# ===== Accept Order (Simulated for Dummy Data) =====
@login_required
def accept_order_sim(request, order_id):
    order = next((o for o in DUMMY_ORDERS if o['id'] == int(order_id)), None)

    if order:
        if order['status'] == 'AVAILABLE':
            order['status'] = 'ON_ROUTE'
            messages.success(request, "Thanks for accepting the order, please deliver it with care.")
        else:
            messages.warning(request, "This order is already accepted.")
    else:
        messages.error(request, "Order not found.")

    return redirect('delivery_dashboard')

# ===== Accept Order (Simulated for Dummy Data) =====
@login_required
def accept_order(request, order_id):
    if request.method == 'POST':  # Ensure POST request
        order = next((o for o in DUMMY_ORDERS if o['id'] == int(order_id)), None)

        if order:
            if order['status'] == 'AVAILABLE':
                order['status'] = 'ON_ROUTE'
                messages.success(request, f"Order {order['order_id']} accepted! Please deliver it with care.")
            else:
                messages.warning(request, f"Order {order['order_id']} is already accepted or delivered.")
        else:
            messages.error(request, "Order not found.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect('delivery_dashboard')
