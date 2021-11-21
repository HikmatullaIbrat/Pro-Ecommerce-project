from django.contrib import admin

# Register your models here.
from .models import GuestEmailModel

admin.site.register(GuestEmailModel)