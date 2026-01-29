from django.urls import path
from .views import *


app_name='product'

urlpatterns=[
    path('',home,name='home'),
    path('proucts/<int:id>/',detail_product,name='product_detail'),
    path('search/',get_product,name='search_product')
]