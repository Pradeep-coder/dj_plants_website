from django.contrib import admin

from .models import About, Cart, ContactProfile, LandingScreen, Order, OrderItem, Plants, Profile, Subscribe, UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user')

@admin.register(LandingScreen)
class LandingScreenAdmin(admin.ModelAdmin):
    list_display = ('id','title')

@admin.register(Plants)
class PlantsAdmin(admin.ModelAdmin):
    list_display = ('id','name','quantity','price')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description','image')

@admin.register(ContactProfile)
class ContactProfileAdmin(admin.ModelAdmin):
    list_display = ('id','timestamp','name')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','product_quantity','created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','fname','lname','phone','country','pincode','total_price','payment_mode','status','tracking_number')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','order','product','price','quantity')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','phone','city','state','country','pincode')

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id','email','timestamp')



