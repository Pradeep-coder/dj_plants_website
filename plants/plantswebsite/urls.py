from django.urls import path
from plantswebsite import views
from .views import PlantsDescriptionView, register

app_name = "plantswebsite"

urlpatterns = [
	path('home/', views.IndexView.as_view(), name="home"),
    path('contact/', views.ContactProfileView.as_view(), name="contact"),
    path('shop/', views.ShopView.as_view(), name="shop"),
	path('shop/<int:id>/', views.PlantsDescription, name="plantsdescription"),
	path('home/<int:id>/', views.PlantsDescription, name="plantsdescription"),
	path('plantsdescription/', PlantsDescriptionView.as_view(), name="pd"),
	# path('add-to-cart/<int:id>/', views.add_to_cart, name="add-to-cart"),
	path('register/', views.register, name="register"),
	path('login/', views.loginpage, name="login"),
	path('logout/', views.logoutpage, name="logout"),

	path('add-to-cart', views.addtocart, name="addtocart"),
	path('cart/', views.viewcart, name="cart"),
	path('update-cart', views.updatecart, name="updatecart"),
	path('delete-cart-item', views.deletecartitem, name="deletecartitem"),

	path('checkout', views.checkout, name="checkout"),
	path('placeorder', views.placeorder, name="placeorder"),

	path('proceed-to-pay', views.razorpaycheck),
	path('my-orders', views.orders, name="myorders"),
	path('viewuserorders/<str:t_no>', views.viewuserorders, name="viewuserorders"),
	]