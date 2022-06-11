from django.contrib import admin

from .models import About, ContactProfile, LandingScreen, Plants, UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user')

@admin.register(LandingScreen)
class LandingScreenAdmin(admin.ModelAdmin):
    list_display = ('id','title')

@admin.register(Plants)
class PlantsAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description','image')

@admin.register(ContactProfile)
class ContactProfileAdmin(admin.ModelAdmin):
    list_display = ('id','timestamp','name')
