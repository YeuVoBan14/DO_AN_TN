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

    path('delete-review/<str:pk>', views.deleteReview, name="delete-review"),

    path('profile/<str:pk>', views.userProfile, name="user-profile"),


    # path for admin
    path('super',views.adminHome,name="adminHome"), 
    path('super/login/',views.adminLogin,name="admin_login"),
    path('super/logout/',views.adminLogout,name="admin_logout"),

    path('test', views.test, name="test")

]
