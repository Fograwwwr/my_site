from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def merge_cart_on_login(sender, user, request, **kwargs):
    if 'cart' in request.session:
        cart, created = Cart.objects.get_or_create(user=user)
        for product_id in request.session['cart']:
            product = Product.objects.get(id=product_id)
            cart.items.add(product)
        del request.session['cart']