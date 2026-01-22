from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):

    ROLE_CHOICES=[
        ('customer','CUSTOMER'),
        ('seller','SELLER'),
        ('admin','ADMIN'),
    ]

    role=models.CharField(max_length=25,choices=ROLE_CHOICES)



class Customer_Profile(models.Model):
    user_id=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=25)
    phone_num=models.CharField(max_length=10)


class Seller_Profile(models.Model):
    user_id=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    store_name=models.CharField(max_length=30)
    gst_number=models.CharField(max_length=25,unique=True)
    is_varified=models.BooleanField(default=True)







