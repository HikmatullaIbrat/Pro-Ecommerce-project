from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.views.generic import TemplateView
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm

from accounts.models import GuestEmailModel
from billings.models import BillingProfile

from addresses.models import Address
from addresses.forms import AddressForm
# Create your views here.
class CartHome(TemplateView):
    template_name = 'carts/home.html'
    
# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     print('New cart created')

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
                "id":x.id,
                'name':x.title,
                'price':x.price,
                "url": x.get_absolute_url(),
                }
    
     for x in cart_obj.products.all()]
    cart_data = {'products':products, 'Tax_total':cart_obj.Tax_total, 'total':cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {"cart":cart_obj})
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
    

def cart_update(request):
    # print(request.POST)
    # This is the id of product which should be shown on /carts/update
    product_id = request.POST.get('product_id')
    
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id = product_id)
        except Product.DoesNotExist: 
            # print('Show message to user, product is gone?')
            return redirect('carts:cart_home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj) # cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()

        if request.is_ajax():
            print('Ajax reuest')
            # ajax message with json to pass whether product added or not to cart
            json_data = {
                'added':added,
                'removed':not added,
                'navbarCartItemsCount':cart_obj.products.count()
            }
            return JsonResponse(json_data)
        
    # 1 first way by reversing
    # return redirect(product_obj.get_absolute_url())
    # 2 second way by namespace
    return redirect('carts:cart_home')

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    
    if cart_created or cart_obj.products.count() == 0:
        return redirect('carts:cart_home')
    # else:
    #     order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    
    #added for billing
    user=   request.user
    billing_profile = None
    
    login_form = LoginForm()
    guest_form = GuestForm()
    shipping_address_form = AddressForm() # address for shipping
    billing_address_form = AddressForm()

    #this portion handles the creation of billing profile for a logged in user or guest which now billingManager does it
    billing_profile , billing_profile_created = BillingProfile.objects.new_or_get(request)

    # guest_email_id = request.session.get('guest_email_id')
    
    # if user.is_authenticated:
    #     billing_profile , billing_profile_created = BillingProfile.objects.get_or_create(user=user,email=user.email)
    # elif guest_email_id is not None:
    #     guest_email_obj = GuestEmailModel.objects.get(id=guest_email_id)
    #     billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(
    #                                                         email=guest_email_obj.email)
    # else:
    #     pass

    # these billing or shipping address ids on .get being created for them after the form passed data
    # and we use these to ids to show form according to their ids existance
    billing_address_id = request.session.get('billing_address_id',None)
    shipping_address_id = request.session.get('shipping_address_id',None)

    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)

        # we create an instance of Order model
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        # to pass shipping_address or billing_address
        if shipping_address_id:         
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
            # print('this is shipping deleted')
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
            # print('this is billing deleted')
        if billing_address_id or shipping_address_id:
            # print('kkkkkkkkkkkkk',billing_address_id, shipping_address_id)
            order_obj.save()
        # if order_qs.count() == 1:
        #     order_obj = order_qs.first()
        # else:
        #     # this portion is handled by modelManager that it deativates the old order with same cart
        #     # older_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
        #     # if older_order_qs.exists():
        #     #     older_order_qs.update(active=False)
        #     order_obj= Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

    if request.method  == 'POST':
        'Some check that order is done'
        is_done = order_obj.check_done()

        # After the cart order finished or paid
        if is_done:
            order_obj.mark_paid()
            # delete the cart id after it completely or ordered 
            request.session['cart_items'] = 0
            del request.session['cart_id']
        return redirect('carts:checkout_success')

    context = {
        'order_obj':order_obj,
        'billing_profile' : billing_profile,
        'login_form' : login_form,
        'guest_form' :guest_form,
        'shipping_address_form': shipping_address_form,
        "billing_address_form": billing_address_form,
        'address_qs': address_qs
    }
    # return render(request, 'carts/checkout_order.html', {"order_obj":order_obj })
    return render(request, 'carts/checkout_order.html', context)


def checkout_done(request):
    return render(request, 'carts/checkout_done.html', {})