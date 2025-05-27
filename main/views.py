from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from .models import Product, Cart, Category, CartItem
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib import messages


class SubCategoryView(ListView):
    model = Product
    template_name = 'main/subcategory.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

def about(request):
    return render(request, 'main/about.html')



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

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(user=None)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


class LoginView(BaseLoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль.')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def get_success_url(self):
        return self.request.GET.get('next', '/')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product_detail.html'

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
    return redirect('cart')