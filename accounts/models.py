from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class GuestEmailModel(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestump = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email

class UserManager(BaseUserManager):
    """ After a making our own users manager model we have constraint key issues with billing profile 
    which have been already made before, so we use a concept of making fixtures which does these things:
    1. Save our pre existing data from our database
    2. clean out the database and refresh it with some new models or apps or any other thing..."""
    def create_user(self,email,full_name,  password=None, is_active=True, is_staff=False, is_admin=False):
        if not full_name:
            raise ValueError('User must have full name')
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')
        
        
        user_obj = self.model(
            full_name =full_name,
            email = self.normalize_email(email),
            # after the creation of full name field we set it
           
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email,full_name, password=None):# function names should be lowercase
        user= self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email,full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    full_name =   models.CharField(max_length=255, blank=True, null=True) # making a required field
    email = models.EmailField(max_length=255, unique=True)
    
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestump = models.DateTimeField(auto_now_add=True)
    # confirm = models.BooleanField(default=False)
    # confirm_date = models.BooleanField(default=False

    REQUIRED_FIELDS = ['full_name'] #[]
    USERNAME_FIELD = 'email'
    # USERNAME FIELD AND PASSWORD ARE REQUIRED BY DEFAULT
   
    
    object = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email
    
    def get_short_name(self):
        return self.email

    # to prevent from this error ('User' object has no attribute 'has_module_perms') we add to other functions
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)