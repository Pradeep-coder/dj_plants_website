from multiprocessing import context
from time import timezone
from django.http import HttpResponse
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

def add_to_cart(request, id):
    item = get_object_or_404(Plants, id=id)
    order_item = PlantsOrderItem.objects.create(item=item)
    order_qs = PlantsOrder.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
    else:
        ordered_date = timezone.now()
        order = PlantsOrder.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:plantsdescription",id=id)


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


