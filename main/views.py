from django.views.generic import TemplateView
from django.shortcuts import render

def about(request):
    return render(request, 'main/about.html')

def view_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        products = cart.items.all()
    else:
        cart_items = request.session.get('cart', [])
        products = Product.objects.filter(id__in=cart_items)

    return render(request, 'cart.html', {'products': products})

class HomeView(TemplateView):
    template_name = 'home.html'


from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')



from django.views.generic import ListView
from .models import Product

class CatalogView(ListView):
    model = Product
    template_name = 'catalog.html'


from django.shortcuts import redirect
from .models import Product, Cart

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        # Для зарегистрированных пользователей
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.add(product)
    else:
        # Для анонимных пользователей (через сессии)
        if 'cart' not in request.session:
            request.session['cart'] = []
        if product_id not in request.session['cart']:
            request.session['cart'].append(product_id)
            request.session.modified = True

    return redirect('catalog')



