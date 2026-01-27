from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from product.models import *

# Create your views here.


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

