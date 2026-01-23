from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,logout,authenticate
from accounts.models import CustomUser,Seller_Profile
from product.models import Category,Product,Product_Image

# Create your views here.
def register_seller(request):
    if request.method.lower()=='post':
        try:
            email=request.POST.get('email')
            password=request.POST.get('password')
            username=request.POST.get('username')
            store_name=request.POST.get('store_name')
            gst_num=request.POST.get('gst_num')

            if CustomUser.objects.filter(username=username).exists():
                return HttpResponse(
                "<div style='color:red'>❌ Username already exists</div>",
                status=400
            )
    

            if CustomUser.objects.filter(email=email).exists():
                return HttpResponse(
                "<div style='color:red'>❌ Email already exists</div>",
                status=400
            )

            user=CustomUser.objects.create_user(username=username,password=password,email=email)
            seller,created=Seller_Profile.objects.get_or_create(user_id=user,store_name=store_name,gst_number=gst_num)
            if created:
                return HttpResponse("account created")
            else:
                return HttpResponse("account created")
        except Exception as e:
            return HttpResponse(e)
    
    return render(request,'seller/register.html')



def home(request):
    user=request.user
    return render(request,'seller/home.html',{'user':user})



def login_seller(request):
    if request.method.lower()=="post":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            if Seller_Profile.objects.filter(user_id=user).exists():
                return  redirect('sellers:home')
            
            else:
                return HttpResponse("this customer")
        else:
            return HttpResponse("Inavlid creds")
    
    return render(request,'seller/login.html')

                




def logout_seller(request):
    logout(request)
    return redirect('sellers:home')





def add_product(request):
    if request.method.lower()=='post':
        seller_id=Seller_Profile.objects.get(user_id=request.user)
        print(request.user,seller_id)
        category=request.POST.get('category').lower()
        cat,created=Category.objects.get_or_create(name=category)
        name=request.POST.get('name')
        price=request.POST.get('price')
        descp=request.POST.get('descp')
        disc_price=request.POST.get('desc_price')
        stock=request.POST.get('stock')
        is_activate=request.POST.get('is_activate')
        if is_activate=='true':
            is_activate=True

        prod=Product.objects.filter(seller_id=seller_id,category_id=cat,name=name)
        if len(prod) == 0 :
            prod,created=Product.objects.get_or_create(seller_id=seller_id,category_id=cat,name=name,price=price,
                discount_percentage=disc_price,stock=stock,is_active=is_activate)

            if created:
                return HttpResponse("Added new Prod")
        else:
            prod=prod[0]
            prod.stock+=int(stock)
            prod.save()
            return HttpResponse("Stock is Updated Prod is already exist")
    

    return render(request,'seller/add_product.html')



def display_products(request,seller_id):
    seller_id=Seller_Profile.objects.get(user_id=seller_id)
    products=Product.objects.filter(seller_id=seller_id)
    all_categories=Category.objects.all()

    
    return render(request,'seller/product_view.html',{'products':products,'category':all_categories})
        


def product_detail(request,pid):
    prod=Product.objects.get(id=pid)
    return render(request,'seller/product_detail.html',{'product':prod})



def edit_product(request,pid):
    prod=Product.objects.get(id=pid)
    if request.method.lower()=='post':
        name=request.POST.get('name')
        price=request.POST.get('price')
        descp=request.POST.get('descp')
        disc_price=request.POST.get('desc_price')
        stock=request.POST.get('stock')
        is_activate=request.POST.get('is_activate')
        if is_activate=='true':
            is_activate=True
        
        prod,created=Product.objects.update_or_create(id=pid,defaults={'name':name,'price':price,'descp':descp,
            'disc_price':disc_price,'stock':stock,'is_activate':is_activate})
        
        return HttpResponse("Product is updated")

    else:
        return render(request,'seller/edit_product.html',{'product':Product})



