from django.contrib import admin
from .models import User, ShippingAdress, Category, Suppiler, Product, Cart, Message, Invoice, InvoiceItem, Order, OrderItem

# Register your models here.
admin.site.register(User)
admin.site.register(ShippingAdress)
admin.site.register(Category)
admin.site.register(Suppiler)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Message)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Order)
admin.site.register(OrderItem)