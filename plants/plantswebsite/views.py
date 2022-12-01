from time import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import get_template

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "plantswebsite/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        landingscreens = LandingScreen.objects.get()
        abouts = About.objects.get()
        plants = Plants.objects.all()
        plants_s = Plants.objects.all()[:6]
        plants_ss = Plants.objects.all()[:4]

        context["landingscreens"] = landingscreens
        context["abouts"] = abouts
        context["plants"] = plants
        context["plants_s"] = plants_s #check out our products section
        context["plants_ss"] = plants_ss #trending plants

        return context

class ContactProfileView(generic.FormView):
    template_name = "plantswebsite/contact.html"
    form_class = ContactProfileForm
    success_url = "/home/"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. We will be in touch soon.")
        return super().form_valid(form)

class ShopView(generic.TemplateView):
    template_name = "plantswebsite/shop.html"
    # form_class = ContactProfileForm
    success_url = "/home/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        shop_plants = Plants.objects.all()

        context["shop_plants"] = shop_plants

        return context

def PlantsDescription(request, id):
    plants_object = Plants.objects.get(id=id)
    return render(request, 'plantswebsite/plants_description.html', {'plants_object':plants_object})

class PlantsDescriptionView(ListView):
    model = Plants
    template_name = "plants_description.html"

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registered Successfully! Login to continue")
            return redirect('/login')
    context = {'form':form}
    return render(request, "plantswebsite/register.html", context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request,"Logged in Already!")
        return redirect("/home")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,"Logged in Successfully!")
                return redirect('/home')
            else:
                messages.error(request,"Invalid Username or Password!")
                return redirect('/login')
        return render(request, 'plantswebsite/login.html')

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/home")

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_check = Plants.objects.get(id=product_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id, product_id=product_id)):
                    return JsonResponse({'status':'Product already in cart'})
                else:
                    product_quantity = int(request.POST.get('product_quantity'))

                    if product_check.quantity >= product_quantity:
                        Cart.objects.create(user=request.user, product_id=product_id, product_quantity=product_quantity)
                        return JsonResponse({'status':'Product addded to cart'})
                    else:
                        return JsonResponse({'status':'Only' + str(product_check.quantity) + "quantity is available"})
            else:
                return JsonResponse({'status':'No product found'})
        else:
            return JsonResponse({'status':'Login to Continue'})
    return redirect("/home")

def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart':cart}
    return render(request,"plantswebsite/cart.html", context)

def updatecart(request):
    if request.method == "POST":
        product_id = int(request.POST.get('product_id'))
        if (Cart.objects.filter(user=request.user, product_id=product_id)):
            product_quantity = int(request.POST.get('product_quantity'))
            cart = Cart.objects.get(product_id=product_id, user=request.user)
            cart.product_quantity = product_quantity
            cart.save()
            return JsonResponse({'status':"Cart Updated Successfully!",'product_quantity':cart.product_quantity})
    return redirect("/home")


def deletecartitem(request):
    if request.method == "POST":
        product_id = int(request.POST.get('product_id'))
        if (Cart.objects.filter(user=request.user, product_id=product_id)):
            cartitem = Cart.objects.get(product_id=product_id, user=request.user)
            cartitem.delete()
        return JsonResponse({'status':"Deleted Successfully!"})
    return redirect("/home")

@login_required(login_url='login')
def checkout(request):
    rawCartItems = Cart.objects.filter(user=request.user)
    for item in rawCartItems:
        if item.product_quantity > item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartItems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartItems:
        total_price = total_price + item.product.price * item.product_quantity

    userProfile = Profile.objects.filter(user=request.user).first()

    context = {'cartItems': cartItems, 'totalPrice':total_price, 'userProfile':userProfile}
    return render(request, "plantswebsite/checkout.html", context)

@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':

        currentUser = User.objects.filter(id=request.user.id).first()

        if not currentUser.first_name:
            currentUser.first_name = request.POST.get('firstname')
            currentUser.last_name = request.POST.get('lastname')
            currentUser.save()

        if not Profile.objects.filter(user=request.user):
            userProfile = Profile()
            userProfile.user = request.user
            userProfile.phone = request.POST.get('phone')
            userProfile.address = request.POST.get('address')
            userProfile.city = request.POST.get('city')
            userProfile.state = request.POST.get('state')
            userProfile.country = request.POST.get('country')
            userProfile.pincode = request.POST.get('pincode')
            userProfile.save()

        newOrder = Order()
        newOrder.user = request.user
        newOrder.fname = request.POST.get('firstname')
        newOrder.lname = request.POST.get('lastname')
        newOrder.email = request.POST.get('email')
        newOrder.phone = request.POST.get('phone')
        newOrder.address = request.POST.get('address')
        newOrder.city = request.POST.get('city')
        newOrder.state = request.POST.get('state')
        newOrder.country = request.POST.get('country')
        newOrder.pincode = request.POST.get('pincode')

        newOrder.payment_mode = request.POST.get('payment_mode')
        newOrder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.price * item.product_quantity

        newOrder.total_price = cart_total_price

        trackNumber = newOrder.fname[:5] + str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_number = trackNumber) is None:
            trackNumber = newOrder.fname[:5] + str(random.randint(1111111,9999999))

        newOrder.tracking_number = trackNumber
        newOrder.save()

        newOrderItems = Cart.objects.filter(user=request.user)
        #To create in OrderItem model
        for items in newOrderItems:
            OrderItem.objects.create(
                order = newOrder,
                product = items.product,
                price = items.product.price,
                quantity = items.product_quantity
            )
            # To decrease from available Plants stock
            orderplants = Plants.objects.filter(id=items.product_id).first()
            orderplants.quantity = orderplants.quantity - items.product_quantity
            orderplants.save()

        # To clear users cart
        Cart.objects.filter(user=request.user).delete()
        
        # return JsonResponse({'status':"Order Placed Successfully!"})

        payMode = request.POST.get('payment_mode')
        if (payMode == "Paid with Razorpay"):
            return JsonResponse({'status':"Order Placed Successfully!"})
        else:
            messages.success(request, "Order Placed Successfully!")

    return redirect('/home')

@login_required(login_url='login')
def razorpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.product.price * item.product_quantity

    return JsonResponse({
        'total_price': total_price
    })

@login_required(login_url='login')
def orders(request):
    userOrders = Order.objects.filter(user=request.user)
    context = {"userOrders":userOrders} 
    return render(request, "plantswebsite/userorders.html", context)

def viewuserorders(request, t_no):
    order = Order.objects.filter(tracking_number=t_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order': order, 'orderitems': orderitems}
    return render(request, "plantswebsite/viewuserorders.html", context)

def subscriber(request):
    subscribeForm = Subscribe()
    if request.method == "POST":
        subscribeForm.email = request.POST.get('SubcribeEmail')
        subscribeForm.save()
        messages.success(request,"Thank You for Subscribing!")
        
    return redirect('/home')
            
def userpasswordreset(request):
    if request.method == 'POST':
        try:
            Usermail = request.POST.get('resetEmail')
            password1 = request.POST.get('password1')
            form = User.objects.get(email=Usermail)
            form.set_password(password1)
            form.save()
            messages.success(request, "Password Reset Done! Login now.")
            return redirect('/login')
        except Exception as e:
            print(e)
            messages.success(request, "User Mail does not exist!")
    return render(request, "plantswebsite/user_password_reset.html")

def plantsSearchList(request):
    plants = Plants.objects.filter(status=0).values_list('name', flat=True)
    plantsList = list(plants)

    return JsonResponse(plantsList, safe=False)

def searchPlantsProducts(request):
    if request.method == "POST":
        searchTerm = request.POST.get('plantsSearch')
        if searchTerm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Plants.objects.filter(name__contains=searchTerm).first()

            if product:
                return redirect('shop/'+str(product.id)+'/')
            else:
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


