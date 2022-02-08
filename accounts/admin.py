from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.

# This function makes the password for readonly in admin panel
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name') # In this way, we will see the admin infos by these attributes in parameter
    readonly_fields = ('last_login', 'date_joined') # Fields that will be for readonly in admin panel
    ordering = ('-date_joined',) # to show in descending order

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
