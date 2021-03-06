from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Organization, Product, Request, Correspondence, Status, TPKeysProduct, TPKey


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'password', 'email', 'first_name', 'last_name', 'organization')
    fieldsets = UserAdmin.fieldsets + (
        ('Organization', {'fields': ('organization',)}),
    )

    list_filter = ('organization',)


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ('inn', 'title', 'index', 'address', 'phone')
    fields = ['inn', 'title', 'index', 'address', 'phone']


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'product')
    exclude = ()


class RequestAdmin(admin.ModelAdmin):
    model = Request
    list_display = ('id', 'client', 'organization', 'product', 'problem',
                    'registration_date', 'status')
    exclude = ()


class CorrespondenceAdmin(admin.ModelAdmin):
    model = Correspondence
    list_display = ('id', 'req', 'from_user', 'answer', 'date')
    exclude = ()
    list_filter = ('date', 'from_user')


class TPKeysProductAdmin(admin.ModelAdmin):
    model = TPKeysProduct
    list_display = ('id', 'key_id', 'product_id')
    exclude = ()


class TPKeyAdmin(admin.ModelAdmin):
    model = TPKey
    list_display = ('key', 'organization')
    exclude = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Correspondence, CorrespondenceAdmin)
admin.site.register(Status)
admin.site.register(TPKeysProduct, TPKeysProductAdmin)
admin.site.register(TPKey, TPKeyAdmin)
