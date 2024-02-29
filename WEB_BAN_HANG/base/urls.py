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

    path('super/product/', views.productAdmin, name="productAdmin"),
    path('super/add-product/', views.addProduct, name="addProduct"),
    path('super/update-product/<str:pk>', views.updateProduct, name="updateProduct"),
    path('super/delete-product/<str:pk>', views.deleteProduct, name="deleteProduct"),

    path('super/suppiler/', views.suppilerAdmin, name="suppilerAdmin"),
    path('super/add-suppiler/', views.addSuppiler, name="addSuppiler"),
    path('super/update-suppiler/<str:pk>', views.updateSuppiler, name="updateSuppiler"),
    path('super/delete-suppiler/<str:pk>', views.deleteSuppiler, name="deleteSuppiler"),

    path('super/category/', views.categoryAdmin, name="categoryAdmin"),
    path('super/add-category/', views.addCategory, name="addCategory"),
    path('super/update-category/<str:pk>', views.updateCategory, name="updateCategory"),
    path('super/delete-category/<str:pk>', views.deleteCategory, name="deleteCategory"),

    path('super/invoice/', views.invoiceAdmin, name="InvoiceAdmin"),
    path('super/invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('super/select-suppiler/', views.select_suppiler, name='select_suppiler'),
    path('super/add-invoice-item/<str:suppiler>/<str:invoice_id>/', views.add_invoice_item, name='add_invoice_item'),


    path('test', views.test, name="test")

]
