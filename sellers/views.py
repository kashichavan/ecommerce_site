from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser, Seller_Profile
from product.models import Category, Product


# ---------------- REGISTER SELLER ----------------
def register_seller(request):
    if request.method.lower() == 'post':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        store_name = request.POST.get('store_name')
        gst_num = request.POST.get('gst_num')

        if CustomUser.objects.filter(username=username).exists():
            return redirect('sellers:register_seller')

        if CustomUser.objects.filter(email=email).exists():
            return redirect('sellers:register_seller')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Seller_Profile.objectscreate(
            user_id=user,
            store_name=store_name,
            gst_number=gst_num
        )

        return redirect('sellers:login_seller')

    return render(request, 'seller/register.html')


# ---------------- LOGIN ----------------
def login_seller(request):
    if request.method.lower() == 'post':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('sellers:home')

        return redirect('sellers:login_seller')

    return render(request, 'seller/login.html')


# ---------------- LOGOUT ----------------
@login_required(login_url='sellers:login_seller')
def logout_seller(request):
    logout(request)
    return redirect('sellers:login_seller')


# ---------------- HOME ----------------
@login_required(login_url='sellers:login_seller')
def home(request):
    return render(request, 'seller/home.html')


# ---------------- ADD PRODUCT ----------------
@login_required(login_url='sellers:login_seller')
def add_product(request):
    if request.method.lower() == 'post':
        seller = Seller_Profile.objects.get(user_id=request.user)

        category_name = request.POST.get('category').lower()
        category, _ = Category.objects.get_or_create(name=category_name)

        name = request.POST.get('name')
        price = request.POST.get('price')
        descp = request.POST.get('descp')
        disc_price = request.POST.get('desc_price') or 0
        stock = int(request.POST.get('stock'))
        is_active = request.POST.get('is_activate') == 'true'

        product = Product.objects.filter(
            seller_id=seller,
            category_id=category,
            name=name
        ).first()

        if product:
            product.stock += stock
            product.save()
        else:
            Product.objects.create(
                seller_id=seller,
                category_id=category,
                name=name,
                price=price,
                descp=descp,
                discount_percentage=disc_price,
                stock=stock,
                is_active=is_active
            )

        return redirect('sellers:display_products', seller_id=request.user.id)

    return render(request, 'seller/add_product.html')


# ---------------- DISPLAY PRODUCTS ----------------
@login_required(login_url='sellers:login_seller')
def display_products(request, seller_id):
    seller = get_object_or_404(Seller_Profile, user_id=seller_id)
    products = Product.objects.filter(seller_id=seller)
    categories = Category.objects.all()

    return render(
        request,
        'seller/product_view.html',
        {
            'products': products,
            'category': categories
        }
    )


# ---------------- PRODUCT DETAIL ----------------
@login_required(login_url='sellers:login_seller')
def product_detail(request, pid):
    product = get_object_or_404(Product, id=pid)
    return render(request, 'seller/product_detail.html', {'product': product})


# ---------------- EDIT PRODUCT ----------------
@login_required(login_url='sellers:login_seller')
def edit_product(request, pid):
    product = get_object_or_404(Product, id=pid)

    if request.method.lower() == 'post':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.descp = request.POST.get('descp')
        product.discount_percentage = request.POST.get('desc_price')
        product.stock = request.POST.get('stock')
        product.is_active = request.POST.get('is_activate') == 'true'

        product.save()
        return redirect('sellers:product_detail', pid=product.id)

    return render(request, 'seller/edit_product.html', {'product': product})




from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, Product_Image

def add_image(request, pid):
    product = get_object_or_404(Product, id=pid)

    if request.method.lower() == "post":
        images = request.FILES.getlist('images')  # 👈 IMPORTANT

        for img in images:
            Product_Image.objects.create(
                prod_id=product,
                image=img
            )

        return redirect('sellers:product_detail', pid=product.id)

    return render(
        request,
        'seller/upload_image.html',
        {'product': product}
    )
