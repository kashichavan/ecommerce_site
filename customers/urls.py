from django.urls  import path
from .views import add_to_cart_session
from .views import *


app_name='customers'

urlpatterns=[
    path('cart/<int:pid>',add_to_cart_session,name='add_to_cart'),
    path('cart_display/',display_cart_session,name='display_cart'),
    path('register/',register,name='customer_register'),
    path('login/',login_customer,name='login_customer'),
    path('logout/',login_customer,name='logout')
]