from django.urls import path
from .views import *
app_name='sellers'


urlpatterns=[
    path('register-seller/',register_seller,name='register_seller'),
    path('login-seller/',login_seller,name='login_seller'),
    path('logout-seller/',logout_seller,name='logout_seller'),
    path('add-product/',add_product,name='add_product'),
    path('home/',home,name='home')
]