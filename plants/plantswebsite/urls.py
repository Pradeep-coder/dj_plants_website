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
	path('add-to-cart/<int:id>/', views.add_to_cart, name="add-to-cart"),
	path('register/', views.register, name="register"),
	path('login/', views.loginpage, name="login"),
	path('logout/', views.logoutpage, name="logout"),
    # path('demo/', views.demo, name="demo"),
	# path('contact/', views.ContactView.as_view(), name="contact"),
	# path('portfolio/', views.PortfolioView.as_view(), name="portfolios"),
	# path('portfolio/<slug:slug>', views.PortfolioDetailView.as_view(), name="portfolio"),
	# path('blog/', views.BlogView.as_view(), name="blogs"),
	# path('blog/<slug:slug>', views.BlogDetailView.as_view(), name="blog"),
	]