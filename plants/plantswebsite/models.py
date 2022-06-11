from email import message
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    class Meta:
        verbose_name_plural = 'User Profiles'
        verbose_name = 'User Profile'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class LandingScreen(models.Model):
    class Meta:
        verbose_name_plural = 'Landing Screens'
        verbose_name = 'Landing Screen'

    title = models.CharField(max_length=244, blank=False, null=True)
    description = models.CharField(max_length=244, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='landingscreen')

    def __str__(self):
        return self.title

class Plants(models.Model):
    class Meta:
        verbose_name_plural = 'Plants'
        verbose_name = 'Plant'

    name = models.CharField(max_length=244, blank=False, null=True)
    price = models.IntegerField(blank=False, null=True)
    description = models.CharField(max_length=244, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='plants')
    highlights_one = models.CharField(max_length=128, blank=True, null=True)
    highlights_two = models.CharField(max_length=128, blank=True, null=True)
    highlights_three = models.CharField(max_length=128, blank=True, null=True)
    highlights_four = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

class About(models.Model):
    class Meta:
        verbose_name_plural = 'Abouts'
        verbose_name = 'About'

    title = models.CharField(max_length=244, blank=True, null=True)
    description = models.CharField(max_length=244, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='abouts')

    def __str__(self):
        return self.title

class ContactProfile(models.Model):
    class Meta:
        verbose_name_plural = 'ContactProfiles'
        verbose_name = 'ContactProfile'
        ordering = ['timestamp']

    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(verbose_name='name',max_length=124)
    email = models.EmailField(verbose_name='email')
    message = models.TextField(verbose_name='message')

    def __str__(self):
        return f'{self.name}'
    



    
