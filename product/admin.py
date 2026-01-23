from django.contrib import admin

from .models import Product_Image
# Register your models here.


class UploadImage(admin.ModelAdmin):
    list_display=['id','image']



admin.site.register(Product_Image,UploadImage)

