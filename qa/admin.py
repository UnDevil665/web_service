from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Organization, Product, Request


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'password', 'email', 'first_name', 'last_name', 'organization_title')


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ('inn', 'title', 'index', 'address', 'phone')
    fields = ['inn', 'title', 'index', 'address', 'phone']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Product)
admin.site.register(Request)

