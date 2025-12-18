from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "starting_price",
        "current_price",
        "winner",
        "is_active",
        "is_closed",
    )
    list_filter = ("category", "is_active", "is_closed")
    search_fields = ("name",)
