from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,logout,authenticate
from accounts.models import CustomUser,Seller_Profile

# Create your views here.
def register_seller(request):
    if request.method.lower()=='post':
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

                



