from django.contrib import admin
from pool.models import Service, FoodService, TravelService, ShoppingService


admin.site.register(
    Service,
    list_display=["id", "description", "get_members"],
    list_display_links=["id", "description", "get_members"],
)
