from django.urls import path
from .views import RegisterView, HomeView, CatalogView
from django.contrib.auth.views import LoginView, LogoutView
from .views import add_to_cart, view_cart
from .views import about

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("main/about/", about, name= "about"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
]



