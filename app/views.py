from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Customer,Cart,Wishlist
from django.db.models  import Count
from .forms import CustomerRegistrationForm,LoginForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.db.models  import Q
from django.http import JsonResponse


def home(request):
    return render(request, 'app/home.html')
def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')


class CategoryView(View):  
    def get(self, request, val):  
        product = Product.objects.filter(category=val)  
        title = Product.objects.filter(category=val).values('title')  
        return render(request, "app/category.html", locals())  

class CategoryTitle(View):  
    def get(self, request, val):  
        product = Product.objects.filter(title=val)  
        title = Product.objects.filter(category=product[0].category).values('title')  
        return render(request, "app/category.html", locals())  

class ProductDetail(View):  
    def get(self, request, pk):  
        product = Product.objects.get(pk=pk)  
        return render(request, "app/productdetail.html", locals())  

class  CustomerRegistrationview(View):
    def get(self,request):
     form = CustomerRegistrationForm()
     return render(request,'app/customerregistration.html',locals())
    def post(self,request):
         form = CustomerRegistrationForm(request.POST)
         if form.is_valid():
          form.save()
          messages.success(request,"Registration Successfull")
         else:
             messages.warning(request,'Invalid Input Data')
         return render(request,'app/customerregistration.html',locals())
     

class ProfileView(View):  
    def get(self, request):  
        form = CustomerProfileForm()  
        return render(request, 'app/profile.html', locals())  

    def post(self, request):  
        form = CustomerProfileForm(request.POST)  
        if form.is_valid():  
            user = request.user  
            name = form.cleaned_data['name']  
            locality = form.cleaned_data['locality']  
            city = form.cleaned_data['city']  
            mobile = form.cleaned_data['mobile']  
            state = form.cleaned_data['state']  
            zipcode = form.cleaned_data['zipcode']  

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)  
            reg.save()  
            messages.success(request, "Congratulations! Profile Save Successfully")  
        else:  
            messages.warning(request, "Invalid Input Data")  
        return render(request, 'app/profile.html', locals())  

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals()) 

class UpdateAddress(View):  
    def get(self, request, pk):  
        add = Customer.objects.get(pk=pk)  
        form = CustomerProfileForm(instance=add)  
        return render(request, 'app/updateAddress.html', locals())  

    def post(self, request, pk):  
        form = CustomerProfileForm(request.POST)  
        if form.is_valid():  
            add = Customer.objects.get(pk=pk)  
            add.name = form.cleaned_data['name']  
            add.locality = form.cleaned_data['locality']  
            add.city = form.cleaned_data['city']  
            add.mobile = form.cleaned_data['mobile']  
            add.state = form.cleaned_data['state']  
            add.zipcode = form.cleaned_data['zipcode']  
            add.save()  
            messages.success(request, "Congratulations! Profile Update Successfully")  
        else:  
            messages.warning(request, "Invalid Input Data")  
        return redirect("address")
    
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    
    # Retrieve the product from the Product model
    product = get_object_or_404(Product, id=product_id)
    
    # Add the product to the cart
    Cart.objects.create(user=user, product=product)
    
    # Redirect to the cart page
    return redirect('/cart')

    
def show_cart(request):  
    user = request.user  
    cart = Cart.objects.filter(user=user) 
    amount = sum(item.quantity * item.product.discounted_price for item in cart)
    # amount=0
    # for p in cart:
    #     value = p.product.discounted_price
    #     amount=amount+value
    totalamount=amount+40 
    return render(request, 'app/addtocart.html', locals())    

def calculate_cart_totals(user):
    cart = Cart.objects.filter(user=user)
    amount = sum(p.quantity * p.product.discounted_price for p in cart)
    totalamount = amount + 40  # Fixed shipping cost
    return amount, totalamount

def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        # Get or create a cart item
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        # If the item is already in the cart, increment the quantity
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Calculate the amount and total amount
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.quantity * item.product.discounted_price for item in cart_items) + 40  # Include shipping cost
        amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        print("plus clicked: ",amount, total_amount, cart_item.product.discounted_price)

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(data)
# Function to handle removing a product from the cart
def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        # Get the cart item
        cart_item = Cart.objects.filter(user=request.user, product=product).first()

        # Decrement quantity or remove item if quantity is 1
        if cart_item:
            if cart_item.quantity > 0:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        # Recalculate the total amount after modification
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.quantity * item.product.discounted_price for item in cart_items) + 40  # Include shipping cost
        total_quantity = sum(item.quantity for item in cart_items)
        amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        data = {
            'quantity': cart_item.quantity if cart_item else 0,
            'totalamount': total_amount,
            'totalquantity': total_quantity,
            'amount':amount
        }
        return JsonResponse(data)

# Function to handle removing a product completely from the cart
def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        # Get and delete the cart item
        cart_item = Cart.objects.filter(user=request.user, product=product).first()
        if cart_item:
            cart_item.delete()

        # Recalculate the total amount after removal
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.quantity * item.product.discounted_price for item in cart_items) + 40  # Include shipping cost
        total_quantity = sum(item.quantity for item in cart_items)

        data = {
            'amount': total_amount,
            'totalquantity': total_quantity
        }
        return JsonResponse(data)
# Function to handle adding a product to the wishlist
def plus_wishlist(request):
    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        # Get or create a wishlist item
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        data = {
            'message': 'Product added to wishlist successfully!'
        }
        return JsonResponse(data)

# Function to handle removing a product from the wishlist
def minus_wishlist(request):
    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        # Remove the wishlist item
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        if wishlist_item:
            wishlist_item.delete()

        data = {
            'message': 'Product removed from wishlist successfully!'
        }
        return JsonResponse(data) 