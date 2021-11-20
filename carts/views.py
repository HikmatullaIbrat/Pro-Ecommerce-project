from django.shortcuts import render , redirect
from django.views.generic import TemplateView
from .models import Cart
from products.models import Product
from orders.models import Order

# Create your views here.
class CartHome(TemplateView):
    template_name = 'carts/home.html'
    
# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     print('New cart created')

def cart_home(request):
    # print(request.session)
    # print(dir(request.session))
    # print(request.session.session_key)
    # print(request.session.set_expiry(300))
    # Providing a name a session
    # session_name = request.session['first_name'] = 'Seerat'
    # request.session['user'] = request.user.username
    # del request.session['cart_id'] # to delete a session
    #cart_id = request.session.get('cart_id',None)
    
    # To get the session for cart
    #request.sessoin['cart_id'] = 12
    # checking whether session exists
   
    # if no session found so we create session
    # if cart_id is None:
    #     cart_obj = Cart.create()
    #     request.session['cart_id'] = cart_obj.id
        
    #     #request.sessoin['cart_id'] = 12
    # # but if session found
    # else:
    #     print('Cart ID exists')
    #     print(cart_id)
    #     qs = Cart.objects.filter(id=cart_id)
    #     # if session found we assign the first obj to cart because it will be the first one
    #     if qs.count() == 1:
    #         print('Cart ID exists')
    #         cart_obj = qs.first()
    #     # if no session found so we create session
    #     else:
    #         cart_obj = cart_create()
    #         request.session['cart_id'] = cart_obj.id

    # return render(request, 'carts/home.html', {})
    # with below to lines we carried all the upper session controlling code to model new_or_get() method
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {"cart":cart_obj})

def cart_update(request):
    print(request.POST)
    # This is the id of product which should be shown on /carts/update
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id = product_id)
        except Product.DoesNotExist: 
            print('Show message to user, product is gone?')
            return redirect('carts:cart_home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj) # cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
        
    # 1 first way by reversing
    # return redirect(product_obj.get_absolute_url())
    # 2 second way by namespace
    return redirect('carts:cart_home')

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request, 'carts/checkout_order.html', {"order_obj":order_obj })