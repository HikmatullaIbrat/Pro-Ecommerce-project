from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Cart
# Create your views here.
class CartHome(TemplateView):
    template_name = 'carts/home.html'
    
def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    print('New cart created')

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
      cart_id = request.session.get('cart_id',None)
    qs= Cart.objects.filter(id = cart_id)
    if qs.count() == 1:
        # print('Cart ID exists')
        cart_obj = qs.first()
        # if user comes to carts page and session saving for him after he logged in so session will also be 
                 # saved with his name
        if request.user.is_authenticated and cart_obj.user is None:
            cart_obj.user = request.user
            cart_obj.save()
    else:
        cart_obj = Cart.objects.new(user = request.user)
        request.session['cart_id'] = cart_obj.id
    return render(request, 'carts/home.html', {})  
