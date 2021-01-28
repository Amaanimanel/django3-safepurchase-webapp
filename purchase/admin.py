from django.contrib import admin
from .models import Purchase

class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Purchase, PurchaseAdmin)
