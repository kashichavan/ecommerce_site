from django.db import models
from accounts.models import Seller_Profile
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=25,unique=True)


class Product(models.Model):
    seller_id=models.ForeignKey(Seller_Profile,on_delete=models.CASCADE)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    price=models.FloatField()
    discount_percentage=models.FloatField()
    stock=models.IntegerField()
    is_active=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)

from cloudinary.models import CloudinaryField

class Product_Image(models.Model):
    prod_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=CloudinaryField('image', blank=True, null=True)