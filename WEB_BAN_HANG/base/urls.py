from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('product/<str:pk>/', views.productPage, name='product'),

    path ('cart', views.cart, name="cart"),
    path ('cart-add/', views.cartAdd, name="cart_add"),
    path ('cart-delete/', views.cartDelete, name="cart_delete"),
    path ('cart-update/', views.cartUpdate, name="cart_update"),

]
