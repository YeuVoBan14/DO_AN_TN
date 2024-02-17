from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
import datetime
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
class User(AbstractUser):
    birth = models.DateField(blank=True,null=True)
    gender = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10,null=True)
    avatar = models.ImageField(null=True,blank=True,upload_to='users/',default= 'users/avatar.svg')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
class ShippingAdress(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)
class Category(models.Model):
    name = models.CharField(max_length=80)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
class Suppiler(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    cat = models.ManyToManyField(Category,blank=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=200)
    cat = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    price_im = models.DecimalField(max_digits=6,decimal_places=2,default=0.0,blank=True)
    price_sell = models.DecimalField(max_digits=6,decimal_places=2,default=0.0,blank=True)
    suppiler = models.ForeignKey(Suppiler,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0,blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True,default="product.jpg",upload_to='product')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
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
    quantity = models.PositiveIntegerField(default=0)
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    shippingadress = models.ForeignKey(ShippingAdress,on_delete=models.SET_NULL,null=True)
    status = models.SmallIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)




