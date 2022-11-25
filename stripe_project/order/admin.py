from django.contrib import admin
from .models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('item',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'paid', 'email', 'created')
    list_filter = ('paid', 'created')
    inlines = (OrderItemInline,)
