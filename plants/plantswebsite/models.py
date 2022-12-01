from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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
    price = models.FloatField(blank=False, null=True)
    original_price = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=244, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='plants')
    quantity = models.IntegerField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-default, 1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-default, 1-Hidden")
    highlights_one = models.CharField(max_length=128, blank=True, null=True)
    highlights_two = models.CharField(max_length=128, blank=True, null=True)
    highlights_three = models.CharField(max_length=128, blank=True, null=True)
    highlights_four = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Plants, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True,blank=True)
    orderstatus = (
        ('PENDING','PENDING'),
        ('OUT FOR SHIPPING','OUT FOR SHIPPING'),
        ('COMPLETED','COMPLETED'),
    )
    status = models.CharField(choices=orderstatus, max_length=150, default='PENDING')
    message = models.TextField(blank=True, null=True)
    tracking_number = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_number)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Plants, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_number)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

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

class Subscribe(models.Model):
    class Meta:
        verbose_name_plural = 'Subscribers'
        verbose_name = 'Subscriber'
        ordering = ['timestamp']

    email = models.EmailField(verbose_name='email', max_length=150, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'

    



    
