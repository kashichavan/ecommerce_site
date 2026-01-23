from django.urls import path
from .views import *
app_name='sellers'


urlpatterns=[
    path('register-seller/',register_seller,name='register_seller'),
    path('login-seller/',login_seller,name='login_seller'),
    path('logout-seller/',logout_seller,name='logout_seller'),
    path('add-product/',add_product,name='add_product'),
    path('home/',home,name='home'),
    path('products/<int:seller_id>/', display_products, name='display_products'),
    path('product/<int:pid>/', product_detail, name='product_detail'),
    path('product/edit/<int:pid>/', edit_product, name='edit_product'),

]