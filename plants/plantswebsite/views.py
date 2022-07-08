from multiprocessing import context
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
        


# def ContactProfileView(request):
#     print(request.POST)
#     context = {}
#     return render(request, "plantswebsite/contact.html", context=context)

# def demo(request):
#     landingscreen = LandingScreen.objects.get()
#     print(landingscreen.title)
#     print(landingscreen.image.url)
#     print(landingscreen.description)

#     return HttpResponse(landingscreen)


