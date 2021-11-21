from django.db import models

# Create your models here.

class GuestEmailModel(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestump = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email