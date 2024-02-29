from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .cart import Cart
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)

# Create your views here.
def test(request):
    return render(request, 'base/admin/login.html')
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
            messages.error(request,'Invalid Password or Email')
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
            messages.success(request,  f"Account Created for {user.username}")
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'form': form}
    return render(request, 'base/main/login_register.html', context)

def home(request):
    # search function
    if 'q' in request.GET:
        q = request.GET['q']
        mutiple_q = Q(  Q(cat__name__icontains=q)|
                        Q(name__contains=q)|
                        Q(suppiler__name__icontains=q)|
                        Q(suppiler__name__icontains=q) )
        products = Product.objects.filter(mutiple_q)
    else:
        products = Product.objects.all()
    #pagination
    page = Paginator(products, 8)
    #get ?page= in the template
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    cats = Category.objects.filter(parent__isnull=True).order_by('name')
    suppilers = Suppiler.objects.all()
    sale_prods = Product.objects.filter(is_sale=True)[:9]
    context = {'products':products,'page':page, 'cats':cats, 'suppilers':suppilers, 'sale_prods': sale_prods}
    return render(request, 'base/main/home.html', context)

def productPage(request, pk):
    product = Product.objects.get(id = pk)
    product_reviews = product.review_set.all()
    product_review_len = len(product_reviews)
    overall_score = sum(review.rating for review in product_reviews if review.rating is not None) / (len(product_reviews)) if product_reviews else 0
    sale_prods = Product.objects.filter(is_sale=True)[:9]
    if request.method == 'POST':
        rating = request.POST.get('rating')
        body = request.POST.get('body')

        if not body:
            messages.error(request, "Please provide a review body.")
        else:
            clean_body = censor_bad_words(body)
            review = Review.objects.create(
                rating=rating,
                user=request.user,
                product=product,
                body=clean_body
            )
            messages.success(request, "Review added successfully.")
            return redirect('product',pk=product.id)
    context = {'product': product, 'product_reviews':product_reviews, 'overall_score':overall_score, 'product_review_len': product_review_len, 'sale_prods':sale_prods}
    return render(request,'base/main/product.html',context)

def deleteReview(request,pk):
    review = Review.objects.get(id=pk)
    if request.user != review.user:
        return HttpResponse('Your are not allowed to do that!!')
    if request.method == 'POST':
        review.delete()
        messages.warning(request,'The review has been deleted!')
        return redirect('product', pk=review.product.id)
    return render(request, 'base/main/delete.html', {'obj': review})
#-------------------------Cart----------------------------
def cart(request):
    #Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    sale_prods = Product.objects.filter(is_sale=True)[:9]
    quantities = cart.get_quants()
    totals = cart.cart_total()
    item_total = cart.item_total()
    context = {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'item_total':item_total, 'sale_prods': sale_prods}
    return render(request, 'base/main/cart.html', context)

def cartAdd(request):
    #Get the cart
    cart = Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #look up product in DB
        product = get_object_or_404(Product, id=product_id)
        #Save to session
        cart.add(product=product, quantity=product_qty)

        #Get Cart Quantity
        cart_quantity = cart.__len__()

        #Return a response
        response = JsonResponse({'qty': cart_quantity })
        messages.success(request,'You have add a new item to the cart!')
        return response
def cartDelete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        #call delete func
        cart.delete(product=product_id)
        #dont need this but use this to check to func is working
        messages.success(request,'Product deleted!')
        response = JsonResponse({'product': product_id})
        return response
def cartUpdate(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        #dont need this but use this to check to func is working
        response = JsonResponse({'qty': product_qty})
        messages.success(request,'Shopping cart have been updated!')
        return response
    
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    reviews = user.review_set.all()
    sale_prods = Product.objects.filter(is_sale=True)[:9]
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            instance = form.instance
            form = UserForm(instance=instance)
            messages.success(request,"Your profile has been update")
            return redirect('user-profile', pk=user.id)
        else:
            messages.error(request,"Please correct the error below.")
            return redirect('user-profile', pk=user.id)
    context = {'user': user, 'form': form, 'reviews': reviews, 'sale_prods':sale_prods}
    return render(request, 'base/main/profile.html', context)

###################### ADMIN SITE #########################
def adminLogin(request):
    try:
        if request.user.is_authenticated:
            return redirect('adminHome')
        
        if request.method == 'POST':
            email = request.POST.get('email').lower()
            password = request.POST.get('password')
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "User does not exist")
                return render(request, 'base/admin/login.html')
                
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('adminHome')
            else:
                messages.error(request, 'You a not a staff')
                return render(request, 'base/admin/login.html')
        
        return render(request, 'base/admin/login.html')
    except Exception as e:
        print(e)

def adminLogout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='/super/login/')
def adminHome(request):
    customers = User.objects.filter(is_superuser=False)
    context = {'customers':customers}
    return render(request, 'base/admin/home.html',context)
## Product
@login_required(login_url='/super/login/')
def productAdmin(request):
    pageView = 'read'
    if 'q' in request.GET:
        q = request.GET['q']
        mutiple_q = Q(  Q(cat__name__icontains=q)|
                        Q(name__contains=q)|
                        Q(suppiler__name__icontains=q)|
                        Q(suppiler__name__icontains=q) )
        products = Product.objects.filter(mutiple_q)
    else:
        products = Product.objects.all()
    page = Paginator(products, 4)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {'products': products, 'page': page, 'pageView':pageView}
    return render(request, 'base/admin/product.html', context)
@login_required(login_url='/super/login/')
def addProduct(request):
    pageView = 'add'
    form = CreateProductForm()
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if product.price_sell < product.price_im:
                messages.error(request, "Sale price cannot be lower than import price.")
                return redirect("addProduct")
            elif product.sale_price:
                if product.sale_price < product.price_im:
                    messages.warning(request, "The sale price is less than the import price!")
                    return redirect("addProduct")
                elif product.sale_price > product.price_sell:
                    messages.error(request, "Sale price cannot be higher than sell price.")
                    return redirect("addProduct")
                elif product.sale_price and not product.is_sale:
                    messages.error(request, "If there is a sale price, please check the 'is sale' option.")
                    return redirect("addProduct")
            else:
                product.save()
                messages.success(request, "Successfully added a new product!")
                return redirect("productAdmin")
    context = { "form": form, 'pageView': pageView }
    return render(request, 'base/admin/product.html', context)
@login_required(login_url='/super/login/')
def updateProduct(request, pk):
    pageView = 'edit'
    product = Product.objects.get(id=pk)
    form = UpdateProductForm(instance=product)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            if product.price_sell < product.price_im:
                messages.error(request, "Sale price cannot be lower than import price.")
                return redirect ("updateProduct", pk=product.id)
            elif product.sale_price < product.price_im:
                messages.warning(request, "The sale price is less than the import price!")
                return redirect ("updateProduct", pk=product.id)
            elif product.sale_price > product.price_sell:
                messages.error(request, "Sale price cannot be higher than sell price.")
                return redirect ("updateProduct", pk=product.id)
            elif product.sale_price and not product.is_sale:
                messages.error(request, "If there is a sale price, please check the 'is sale' option.")
                return redirect ("updateProduct", pk=product.id)
            else:
                product.save()
                instance = form.instance
                form = UpdateProductForm(instance=instance)
                messages.success(request,"Your product has been updated")
                return redirect("productAdmin")
        else:
            messages.error(request,"Please correct the error below.")
            return redirect('updateProduct', pk=product.id)
    context = {'form':form, 'pageView':pageView}
    return render(request, 'base/admin/product.html', context)
@login_required(login_url='/super/login/')
def deleteProduct(request, pk):
    pageView = 'delete'
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        messages.warning(request,'The selected product has been deleted!')
        return redirect('productAdmin')
    return render(request,'base/admin/product.html',{'obj': product, 'pageView':pageView})

## Suppiler
@login_required(login_url='/super/login/')
def suppilerAdmin(request):
    pageView = 'read'
    if 'q' in request.GET:
        q = request.GET['q']
        mutiple_q = Q(  Q(name__contains=q)|
                        Q(phone__icontains=q)|
                        Q(address__icontains=q) )
        suppilers = Suppiler.objects.filter(mutiple_q)
    else:
        suppilers = Suppiler.objects.all()
    page = Paginator(suppilers, 4)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {'suppilers': suppilers,'page':page, 'pageView':pageView}
    return render(request, 'base/admin/suppiler.html', context)
@login_required(login_url='/super/login/')
def addSuppiler(request):
    pageView = 'add'
    form = CreateSuppilerForm()
    if request.method == 'POST':
        form = CreateSuppilerForm(request.POST)
        if form.is_valid():
            suppiler = form.save(commit=False)
            categories = form.cleaned_data['cat']
            if len(suppiler.phone) != 10:
                messages.error(request, "Phone number must have exactly 10 digits.")
                return redirect("addSuppiler")
            else:
                suppiler.save()
                suppiler.cat.set(categories)
                suppiler.save()
                messages.success(request, "Successfully added a new company!")
                return redirect("suppilerAdmin")
    context = { "form": form, 'pageView': pageView }
    return render(request, 'base/admin/suppiler.html', context)
@login_required(login_url='/super/login/')
def updateSuppiler(request, pk):
    pageView = 'edit'
    suppiler = Suppiler.objects.get(id=pk)
    form = UpdateSuppilerForm(instance=suppiler)
    if request.method == 'POST':
        form = UpdateSuppilerForm(request.POST, instance=suppiler)
        if form.is_valid():
            product = form.save(commit=False)
            categories = form.cleaned_data['cat']
            if len(suppiler.phone) != 10:
                messages.error(request, "Phone number must have exactly 10 digits.")
                return redirect("addSuppiler")
            else:
                suppiler.save()
                suppiler.cat.set(categories)
                suppiler.save()
                instance = form.instance
                form = UpdateSuppilerForm(instance=instance)
                messages.success(request,"Your suppiler has been updated")
                return redirect("suppilerAdmin")
        else:
            messages.error(request,"Please correct the error below.")
            return redirect('updateSuppiler', pk=product.id)
    context = {'form':form, 'pageView':pageView}
    return render(request, 'base/admin/suppiler.html', context)
@login_required(login_url='/super/login/')
def deleteSuppiler(request, pk):
    pageView = 'delete'
    suppiler = Suppiler.objects.get(id=pk)
    if request.method == 'POST':
        suppiler.delete()
        messages.warning(request,'The selected suppiler has been deleted!')
        return redirect('suppilerAdmin')
    return render(request,'base/admin/product.html',{'obj': suppiler, 'pageView':pageView})
#------------------------------CATEGORIES----------------
@login_required(login_url="/super/login/")
def categoryAdmin(request):
    pageView = 'read'
    if 'q' in request.GET:
        q = request.GET['q']
        mutiple_q = Q( Q(name__contains=q) )
        categories = Category.objects.filter(mutiple_q)
    else:
        categories = Category.objects.all()
    page = Paginator(categories, 4)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {'categories': categories,'page':page, 'pageView':pageView}
    return render(request, 'base/admin/category.html', context)
@login_required(login_url="/super/login/")
def addCategory(request):
    pageView = 'add'
    form = CreateCategoryForm()
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added a new category!")
            return redirect("categoryAdmin")
    context = { "form": form, 'pageView': pageView }
    return render(request, 'base/admin/category.html', context)
@login_required(login_url='/super/login/')
def updateCategory(request, pk):
    pageView = 'edit'
    category = Category.objects.get(id=pk)
    form = UpdateCategoryForm(instance=category)
    if request.method == 'POST':
        form = UpdateCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            instance = form.instance
            form = UpdateCategoryForm(instance=instance)
            messages.success(request,"Your category has been updated")
            return redirect("categoryAdmin")
        else:
            messages.error(request,"Please correct the error below.")
            return redirect('updateCategory', pk=category.id)
    context = {'form':form, 'pageView':pageView}
    return render(request, 'base/admin/category.html', context)
@login_required(login_url='/super/login/')
def deleteCategory(request, pk):
    pageView = 'delete'
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        category.delete()
        messages.warning(request,'The selected category has been deleted!')
        return redirect('categoryAdmin')
    return render(request,'base/admin/product.html',{'obj': category, 'pageView':pageView})
#----------------------------Invoice------------------------------
@login_required(login_url='/super/login/')
def invoiceAdmin(request):
    pageView = 'read'
    if 'q' in request.GET:
        q = request.GET['q']
        mutiple_q = Q( Q(suppiler__name__icontains=q) )
        invoices = Invoice.objects.filter(mutiple_q)
    else:
        invoices = Invoice.objects.all()
    page = Paginator(invoices, 4)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {'invoices':invoices, 'page':page, 'pageView':pageView}
    return render(request, 'base/admin/invoice.html',context)
def invoice_detail(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    return render(request, 'base/admin/invoice_detail.html', {'invoice': invoice})
def select_suppiler(request):
    if request.method == "POST":
        suppiler_form = InvoiceForm(request.POST)
        if suppiler_form.is_valid():
            suppiler = suppiler_form.cleaned_data['suppiler']
            suppiler_id = Suppiler.objects.get(name=suppiler).id
            invoice = Invoice.objects.create(suppiler_id=suppiler_id)
            return redirect('add_invoice_item', suppiler=suppiler_id, invoice_id=invoice.id)
    else:
        suppiler_form = InvoiceForm()
    return render(request, 'base/admin/select_suppiler.html', {'suppiler_form': suppiler_form})
def add_invoice_item(request, suppiler, invoice_id):
    products = Product.objects.filter(suppiler=suppiler)
    if request.method == 'POST':
        print(request.POST)
        invoice = Invoice.objects.get(id=invoice_id)
        for product in products:
            quantity = request.POST.get('quantity_{}'.format(product.id))
            if quantity and int(quantity) > 0:  
                product_id = request.POST.get('product_{}'.format(product.id))
                try:
                    item = InvoiceItem.objects.create(invoice=invoice, product_id=product_id, quantity=quantity)
                    print("Created InvoiceItem for product {} with quantity {}".format(product_id, quantity))
                except Exception as e:
                    print("Error creating InvoiceItem for product {}: {}".format(product_id, str(e)))
        return redirect('invoice_detail', pk=invoice.pk)
    return render(request, 'base/admin/add_invoice_item.html', {'products': products})


