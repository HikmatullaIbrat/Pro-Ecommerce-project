from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import GuestEmailModel

from django.contrib.auth.models import  Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # search_fields = ['email']
    # form = UserAdminChangeForm # edit (update) View
    # add_form = UserAdminCreationForm  # create View

    # it means we don't use the buitin Django forms for user
    # class Meta:
        # model = User

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the user model.
    # The ovveride the definitions on the base UserAdmin that reference specific fields on auth.User
    list_display = ('full_name', 'admin')
    list_filter = ('admin','staff', 'active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal Info', {'fields': ('')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin','staff', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin ovverides get_fieldsets to use this 
    # attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

# Remove Group Model form admin. we're not using it.
admin.site.unregister(Group)
class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestEmailModel

admin.site.register(GuestEmailModel, GuestEmailAdmin)