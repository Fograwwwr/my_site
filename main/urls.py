from django.urls import path
from .views import RegisterView, HomeView, CatalogView, ProductDetailView, SubCategoryView, add_to_cart, view_cart, about
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("about/", about, name= "about"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
    path('catalog/<int:category_id>/', SubCategoryView.as_view(), name='subcategory'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    
]



