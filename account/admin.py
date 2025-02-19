from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('email','username','first_name','last_name','phone_number','date_joined','last_login','is_active',)
    list_display_links=('email','username',) #field e link add kore
    readonly_fields=('date_joined','last_login',)
    ordering=('-date_joined',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()
admin.site.register(Account,AccountAdmin)