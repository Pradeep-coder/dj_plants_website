from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
from django.views import generic
from django.contrib import messages

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


