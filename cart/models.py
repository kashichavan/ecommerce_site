from django.db import models
from accounts.models import Customer_Profile
from product.models import Product

# Create your models here.
class Cart(models.Model):
    customer_id=models.OneToOneField(Customer_Profile,on_delete=models.CASCADE)
    updated_date=models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart_id=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()


