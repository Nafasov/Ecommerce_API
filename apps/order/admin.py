from django.contrib import admin

from .models import (
    CartItem,
    Order,
    Promo
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quantity', 'unit_price')
    list_filter = ('quantity', )
    search_fields = ('user', )
    readonly_fields = ('modified_date', 'created_date')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_delivered', 'created_date', 'modified_date')
    date_hierarchy = 'created_date'
    search_fields = ('user', )
    readonly_fields = ('modified_date', 'created_date')


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'discount', 'min_price', 'created_date')
    date_hierarchy = 'created_date'
    search_fields = ('user', )
    readonly_fields = ('created_date',)
    list_filter = ('discount',)

