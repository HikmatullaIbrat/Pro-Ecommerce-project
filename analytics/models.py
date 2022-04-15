from django.db import models

# Create your models here.

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .utils import get_client_ip
from .signals import object_viewed_signal

from accounts.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.db import models
from django.db.models.signals import pre_save, post_save

User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user           = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address     = models.CharField(max_length=220, blank=True, null=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE) # User, Product, Order, Cart, Address
    object_id      = models.PositiveIntegerField() # User id, product id, Order id
    content_object = GenericForeignKey('content_type', 'object_id') # Product instance
    timestump      = models.DateTimeField(auto_now_add=True)


    def __str__(self):
     return  "%s viewed on %s" %(self.content_object, self.timestump)


    class Meta:
        ordering = ['-timestump']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Object Viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)

    # print(sender)
    # print(instance)
    # print(request)
    # print(request.user)
    new_view_obj = ObjectViewed.objects.create(
        user = request.user,
        content_type = c_type,
        object_id = instance.id,
        ip_address = get_client_ip(request)
    )

object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user          = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address     = models.CharField(max_length=220, blank=True, null=True)
    session_key    = models.CharField(max_length=220, blank=True, null=True)
    # sess  = SessionStore()
    timestump      = models.DateTimeField(auto_now_add=True)
    active         = models.BooleanField(default=True)
    ended          = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()

        except:
            pass
        return self.ended



def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    print(instance)
    user = instance
    ip_address = get_client_ip(request)
    if not  request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    print(session_key)
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )


    

user_logged_in.connect(user_logged_in_receiver)