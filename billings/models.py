from django.db import models
from django.db.models.signals import post_save
# Create your models here.

from django.conf import settings

User = settings.AUTH_USER_MODEL

class BillingProfile(models.Model):
    # unique=True means one user has one billing profile but we don't do it on onToOneField
    # user = models.ForeignKey(User, null=True, unique=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete= models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestump = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print('Actual send to Stripe/braintree')
#         instance.customer_id = newID
#         instance.save()
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance , email=instance.email)

post_save.connect(user_created_receiver, sender=User)
