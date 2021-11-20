from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed
import math
# Create your models here.

from products.models import Product

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    
    def new_or_get(self,request):
        cart_id = request.session.get('cart_id',None)
        qs= self.get_queryset().filter(id = cart_id)
        if qs.count() == 1:
            new_obj = False
            # print('Cart ID exists')
            cart_obj = qs.first()
        # if user comes to carts page and session is saving befor logging in for
        #  him, after he logged in, so session will also be saved with his name
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user = request.user)
            new_obj= True
            request.session['cart_id'] = cart_obj.id
        return cart_obj , new_obj 


    def new(self, user=None):
        user_obj = None
        # (user.is_authenticated)
        if user is not None:
            if user.is_authenticated:
                user_obj=user
        return self.model.objects.create(user = user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,blank=True)
    total = models.DecimalField(default=0.00, max_digits=100,decimal_places=2)
    Tax_total = models.DecimalField(default=0.00, max_digits=100,decimal_places=2)
    updated = models.DateTimeField(auto_now= True)
    timestump = models.DateTimeField(auto_now_add=True)
    objects = CartManager()
    def __str__(self):
        return str(self.id)


# The total calculation
def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    # print(action)
    # print(instance.products.all())
    # print(instance.total)
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':

        products = instance.products.all()

        total = 0
        for x in products:
            total += x.price
        # print('The total',total)
        instance.total = total 
        instance.save()
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

# The total with tax
def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.total > 0:
        #new_total =  math.fsum([instance.total, 10])
        #instance.Tax_total = format(new_total,'.2f')
        # eight percent Tax: we used float function to avoid the decimal.float error
        instance.Tax_total = float(instance.total) * float(1.08)
    else:
        instance.Tax_total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)