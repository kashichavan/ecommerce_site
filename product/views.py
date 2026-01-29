from django.shortcuts import render,HttpResponse
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



def get_product(request):

    query=request.GET.get('q')

    if query:
        products=Product.objects.filter(name__icontains=query)
        for i in products:
            i.discount_price=i.create_discount_price()
    else:
        return HttpResponse("product is unavaiblre with name {query}")
        
    return render(request,'customer/home.html',{'products':products})

