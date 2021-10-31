from django.db import models

import os
import random

# Create your models here.
# remember that every model must be registered on admin.py




def get_filename_ext(filepath):
    base_name = os.path.basename(filepath) # basename returns the final component of file
    name , ext =os.path.splitext(base_name)
    return name , ext


# changing the filename and adding a random number to filename
def upload_image_path(instance, filename):
    print(instance)
    print(filename)     # filename is the type of file like jpg or png
    new_filename = random.randint(1,39138493833)
    # calling the upper function
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename = new_filename, ext = ext )
    return 'product/{new_filename}/{final_filename}'.format(
        new_filename = new_filename,
        final_filename = final_filename
    )

class ProductManager(models.Manager):
    def featured(self):
        return self.get_queryset().filter(featured = True)
    def get_by_id(self,id):
        qs = self.get_queryset().filter(id = id) #Product.objects == self.get_queryset()
        if qs.count() ==1:
            return qs.first()
        return None


# Product table  components
class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()

     # slug field to show the product  name on url
    slug = models.SlugField(default= 'just_some_name')
    
    # those two arguments are required on Decimal field and we can set null = True but default is better
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)

    # we should use ImageField for just allowing images but it requires the Pillow 
    # Pillow should be downloaded with python -m pip install Pillow
    # After installing the Pillow run the makemigrations and migrate commands
    # but still something this technic is not allowed for large file upload
    # pillow installed
    image = models.ImageField(upload_to= upload_image_path, null = True, blank = True)

    featured = models.BooleanField(default=False )
    
   


    
    objects = ProductManager()

    def __str__(self):
        return self.title   


