from django.shortcuts import render, redirect
from billings.models import BillingProfile
from django.utils.http import  is_safe_url
from .forms import AddressForm
from .models import Address

# Create your views here.

#if we want to reuse an address which is already exists or used for other orders
def checkout_address_reuse_view(request):
    """this request 'checkout_address_create' comes from central urls by to this view,
    by checkout_order.html page and this func work based
    on that request and sends  the data to checkout view on carts and after that carts' 
    checkout view sends the data back to checkout_order.html"""
    if request.user.is_authenticated:
        # next keyword is used on urls to redirect to the specified url which assigned to next
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method=="POST":
            print(request.POST)
            shipping_address= request.POST.get('shipping_address', None)
            address_type    =request.POST.get('address_type','shipping')
            billing_profile , billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                
                qs=Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + '_address_id'] = shipping_address
                # print(address_type + '_address_id')
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)

    return redirect('carts:checkout')


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context= {
        'form' : form
    }
    # next keyword is used on urls to redirect to the specified url which assigned to next
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    
    if form.is_valid():
        # print(request.POST)
        #we can use is_safe_url with this method
        instance=form.save(commit=False)
        billing_profile , billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None: 
            instance.billing_profile=billing_profile
            address_type    =request.POST.get('address_type','shipping')
            instance.address_type = address_type 
            # print('Every thing is good dddddddddddddddd')
            instance.save()
            request.session[address_type + '_address_id'] = instance.id
            # print(address_type + '_address_id')
        else:
            print('error here')
            return redirect('carts:checkout') 
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('carts:checkout')  # redirect to home page

    return redirect('carts:checkout')


    
    
    

   