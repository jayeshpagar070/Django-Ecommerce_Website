from django.contrib import admin
from .models import Contact,Product, Orders, OrderUpdate

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phonenumber')
    search_fields = ('name', 'email')

admin.site.register(Contact, ContactAdmin)

admin.site.register(Product)

admin.site.register(Orders)

admin.site.register(OrderUpdate)


