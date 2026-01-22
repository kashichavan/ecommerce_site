from django.contrib import admin
from .models import *
# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','password','email']
    ordering=['first_name']
    search_fields=['first_name']



class SellerAdmin(admin.ModelAdmin):
    list_display=['id','user_id','store_name','gst_number','is_varified']


class CustomerAdmin(admin.ModelAdmin):
    list_display=['user_id','full_name','phone_num']




admin.site.register(Customer_Profile,CustomerAdmin)
admin.site.register(Seller_Profile,SellerAdmin)
admin.site.register(CustomUser,CustomUserAdmin)
