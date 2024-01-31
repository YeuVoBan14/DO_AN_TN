from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    birth = models.DateField()
    gender = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    # avatar = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
class ShippingAdress(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)
class Category(models.Model):
    name = models.CharField(max_length=80)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
class Suppiler(models.Mode):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    product = models.ManyToManyField(Category,blank=True)
class Product(models.Model):
    name = models.CharField(max_length=200)
    cat = models.ForeignKey(Category,on_delete=models.SET_NULL)
    price_im = models.DecimalField(max_digits=5,decimal_places=2,default=0.0,blank=True)
    price_sell = models.DecimalField(max_digits=5,decimal_places=2,default=0.0,blank=True)
    suppiler = models.ForeignKey(Suppiler,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0,blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
class Invoice(models.Model):
    suppiler = models.ForeignKey(Suppiler,on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
class OrderStatus:
    ORDER_NEW = 1
    ORDER_PROCESSING = 2
    ORDER_DELIVERED = 3

    choices = (
        (ORDER_NEW, 'New'),
        (ORDER_PROCESSING, 'Processing'),
        (ORDER_DELIVERED, 'Delivered'),
    )
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    shippingadress = models.ForeignKey(ShippingAdress,on_delete=models.SET_NULL)
    status = models.SmallIntegerField(choices=[(i,OrderStatus[i])for i in range(len(OrderStatus))], default=OrderStatus.ORDER_NEW)
    created = models.DateTimeField(auto_now_add=True)
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)




