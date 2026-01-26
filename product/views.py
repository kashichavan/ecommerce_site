from django.shortcuts import render
from .models import *



# Create your views here.
def home(request):
    products=Product.objects.all()
    for i in products:
        i.discount_price=i.create_discount_price()
        
    return render(request,'customer/home.html',{'products':products})



def detail_product(request,id):
    prod=Product.objects.get(id=id)
    prod.discount_price=prod.create_discount_price()
    return render(request,'customer/detail_product.html',{'prod':prod})

