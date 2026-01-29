from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from product.models import *
from django.http import JsonResponse

from accounts.models import *


# Create your views here.


from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # ---------- Basic Validation ----------
        if not all([full_name, email, phone_num, password, password2]):
            messages.error(request, "All fields are required")
            return redirect('register')

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        # ---------- Create User ----------
        user = CustomUser.objects.create_user(
            email=email,
            username=full_name,
            password=password,
            role='customer'
        )

        # ---------- Create Profile ----------
        Customer_Profile.objects.create(
            user=user,
            full_name=full_name,
            phone_num=phone_num
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'customer/register.html')




from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from accounts.models import CustomUser, Seller_Profile


def login_customer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate first (STANDARD)
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect('customers:login_customer')

        # Role-based restriction
        if Seller_Profile.objects.filter(user_id=user).exists():
            messages.error(request, "Please login from Seller portal")
            return redirect('sellers:login_seller')

        # Login
        login(request, user)
        messages.success(request, "Login successful")
        return redirect('product:home')

    return render(request, 'customer/login.html')


def logout_customer(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('product:home')



def add_to_cart_session(request,pid):
    cart=request.session.get('cart',{})
    prod=get_object_or_404(Product,id=pid)
    
    prod_id=str(prod.id)

    if prod_id in cart:

        cart[prod_id]['quantity']= cart[prod_id]['quantity']+1         
    else:
        cart[prod_id]={'quantity':1}
    
    request.session['cart']=cart
    request.session.modified=True
    
    return  redirect('customers:display_cart')



def display_cart_session(request):

    cart = request.session.get('cart', {})

    if not cart:
        return render(request, 'customer/display_cart.html', {'cart_items': []})

    total_sum = 0
    cart_items = []

    # Convert session keys to int
    product_ids = [int(pid) for pid in cart.keys()]

    # Fetch all products in ONE query
    products = Product.objects.filter(id__in=product_ids, is_active=True)

    product_map = {p.id: p for p in products}

    # Fetch images in ONE query
    images = Product_Image.objects.filter(prod_id__in=products)
    image_map = {img.prod_id.id: img for img in images}

    for pid, item in cart.items():
        product = product_map.get(int(pid))
        if not product:
            continue

        quantity = item['quantity']
        unit_price = product.create_discount_price()
        final_price = quantity * unit_price

        total_sum += final_price

        cart_items.append({
            'product': product,
            'image': image_map.get(product.id),
            'quantity': quantity,
            'final_price': final_price
        })

    return render(
        request,
        'customer/display_cart.html',
        {
            'cart_items': cart_items,
            'total_sum': total_sum,
            'total_products': len(cart_items)
        }
    )


def get_cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return JsonResponse({'count': cart_count})

