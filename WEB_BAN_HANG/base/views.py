from django.shortcuts import render, redirect
from .models import User, ShippingAdress, Category, Suppiler, Product, Cart, Message, Invoice, InvoiceItem, Order, OrderItem
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .forms import MyUserCreationForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def loginPage(request):
    page = 'login'
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,"User does not exist")
            # return redirect('/login/')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Password or Email ID')
    context = {'page': page}
    return render(request,'base/main/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            #after user was created, want to access (clean the data) the user right way, use commit false
            user = form.save(commit=False)
            #clean the data
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'form': form}
    return render(request, 'base/main/login_register.html', context)

def home(request):
    # search function
    if 'q' in request.GET:
        q = request.GET['q']
        mutiple_q = Q(Q(cat__name__icontains=q)|
                      Q(name__contains=q)|
                      Q(suppiler__name__icontains=q))
        products = Product.objects.filter(mutiple_q)
    else:
        products = Product.objects.all()
    #pagination
    page = Paginator(products, 2)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {'products':products,'page':page}
    return render(request, 'base/main/home.html', context)

def productPage(request, pk):
    product = Product.objects.get(id = pk)
    # reviews = Review.objects.filter(product = product).order_by("-date")
    context = {'product': product}
    return render(request,'base/main/product.html',context)


