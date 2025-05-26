from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import redirect
from .models import Product, Cart, Category
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib import messages

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


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')


class CatalogView(ListView):
    model = Product
    template_name = 'catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_categories = Category.objects.filter(parent__isnull=True)
        print(f"Top categories: {top_categories}")
        context['top_categories'] = top_categories
        return context



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

class LoginView(BaseLoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль.')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def get_success_url(self):
        return self.request.GET.get('next', '/')

