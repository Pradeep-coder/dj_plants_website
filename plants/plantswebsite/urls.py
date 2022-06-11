from django.urls import path
from plantswebsite import views

app_name = "plantswebsite"

urlpatterns = [
	path('home/', views.IndexView.as_view(), name="home"),
    path('contact/', views.ContactProfileView.as_view(), name="contact"),
    path('shop/', views.ShopView.as_view(), name="shop"),
	path('shop/<int:id>/', views.PlantsDescription, name="plantsdescription"),
	path('home/<int:id>/', views.PlantsDescription, name="plantsdescription"),
    # path('demo/', views.demo, name="demo"),
	# path('contact/', views.ContactView.as_view(), name="contact"),
	# path('portfolio/', views.PortfolioView.as_view(), name="portfolios"),
	# path('portfolio/<slug:slug>', views.PortfolioDetailView.as_view(), name="portfolio"),
	# path('blog/', views.BlogView.as_view(), name="blogs"),
	# path('blog/<slug:slug>', views.BlogDetailView.as_view(), name="blog"),
	]